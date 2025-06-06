# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""Policy implementing Key Vault's challenge authentication protocol.

Normally the protocol is only used for the client's first service request, upon which:
1. The challenge authentication policy sends a copy of the request, without authorization or content.
2. Key Vault responds 401 with a header (the 'challenge') detailing how the client should authenticate such a request.
3. The policy authenticates according to the challenge and sends the original request with authorization.

The policy caches the challenge and thus knows how to authenticate future requests. However, authentication
requirements can change. For example, a vault may move to a new tenant. In such a case the policy will attempt the
protocol again.
"""

from copy import deepcopy
import sys
import time
from typing import Any, Callable, cast, Optional, overload, TypeVar, Union
from urllib.parse import urlparse

from typing_extensions import ParamSpec

from azure.core.credentials import AccessToken, AccessTokenInfo, TokenRequestOptions
from azure.core.credentials_async import AsyncSupportsTokenInfo, AsyncTokenCredential, AsyncTokenProvider
from azure.core.pipeline import PipelineRequest, PipelineResponse
from azure.core.pipeline.policies import AsyncBearerTokenCredentialPolicy
from azure.core.rest import AsyncHttpResponse, HttpRequest

from .http_challenge import HttpChallenge
from . import http_challenge_cache as ChallengeCache
from .challenge_auth_policy import _enforce_tls, _has_claims, _update_challenge

if sys.version_info < (3, 9):
    from typing import Awaitable
else:
    from collections.abc import Awaitable


P = ParamSpec("P")
T = TypeVar("T")


@overload
async def await_result(func: Callable[P, Awaitable[T]], *args: P.args, **kwargs: P.kwargs) -> T: ...


@overload
async def await_result(func: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T: ...


async def await_result(func: Callable[P, Union[T, Awaitable[T]]], *args: P.args, **kwargs: P.kwargs) -> T:
    """If func returns an awaitable, await it.

    :param func: The function to run.
    :type func: callable
    :param args: The positional arguments to pass to the function.
    :type args: list
    :rtype: any
    :return: The result of the function
    """
    result = func(*args, **kwargs)
    if isinstance(result, Awaitable):
        return await result
    return result


class AsyncChallengeAuthPolicy(AsyncBearerTokenCredentialPolicy):
    """Policy for handling HTTP authentication challenges.

    :param credential: An object which can provide an access token for the vault, such as a credential from
        :mod:`azure.identity.aio`
    :type credential: ~azure.core.credentials_async.AsyncTokenProvider
    """

    def __init__(self, credential: AsyncTokenProvider, *scopes: str, **kwargs: Any) -> None:
        # Pass `enable_cae` so `enable_cae=True` is always passed through self.authorize_request
        super().__init__(credential, *scopes, enable_cae=True, **kwargs)
        self._credential: AsyncTokenProvider = credential
        self._token: Optional[Union["AccessToken", "AccessTokenInfo"]] = None
        self._verify_challenge_resource = kwargs.pop("verify_challenge_resource", True)
        self._request_copy: Optional[HttpRequest] = None

    async def send(self, request: PipelineRequest[HttpRequest]) -> PipelineResponse[HttpRequest, AsyncHttpResponse]:
        """Authorize request with a bearer token and send it to the next policy.

        We implement this method to account for the valid scenario where a Key Vault authentication challenge is
        immediately followed by a CAE claims challenge. The base class's implementation would return the second 401 to
        the caller, but we should handle that second challenge as well (and only return any third 401 response).

        :param request: The pipeline request object
        :type request: ~azure.core.pipeline.PipelineRequest
        :return: The pipeline response object
        :rtype: ~azure.core.pipeline.PipelineResponse
        """
        await await_result(self.on_request, request)
        response: PipelineResponse[HttpRequest, AsyncHttpResponse]
        try:
            response = await self.next.send(request)
        except Exception:  # pylint:disable=broad-except
            await await_result(self.on_exception, request)
            raise
        await await_result(self.on_response, request, response)

        if response.http_response.status_code == 401:
            return await self.handle_challenge_flow(request, response)
        return response

    async def handle_challenge_flow(
        self,
        request: PipelineRequest[HttpRequest],
        response: PipelineResponse[HttpRequest, AsyncHttpResponse],
        consecutive_challenge: bool = False,
    ) -> PipelineResponse[HttpRequest, AsyncHttpResponse]:
        """Handle the challenge flow of Key Vault and CAE authentication.

        :param request: The pipeline request object
        :type request: ~azure.core.pipeline.PipelineRequest
        :param response: The pipeline response object
        :type response: ~azure.core.pipeline.PipelineResponse
        :param bool consecutive_challenge: Whether the challenge is arriving immediately after another challenge.
            Consecutive challenges can only be valid if a Key Vault challenge is followed by a CAE claims challenge.
            True if the preceding challenge was a Key Vault challenge; False otherwise.

        :return: The pipeline response object
        :rtype: ~azure.core.pipeline.PipelineResponse
        """
        self._token = None  # any cached token is invalid
        if "WWW-Authenticate" in response.http_response.headers:
            # If the previous challenge was a KV challenge and this one is too, return the 401
            claims_challenge = _has_claims(response.http_response.headers["WWW-Authenticate"])
            if consecutive_challenge and not claims_challenge:
                return response

            request_authorized = await self.on_challenge(request, response)
            if request_authorized:
                # if we receive a challenge response, we retrieve a new token
                # which matches the new target. In this case, we don't want to remove
                # token from the request so clear the 'insecure_domain_change' tag
                request.context.options.pop("insecure_domain_change", False)
                try:
                    response = await self.next.send(request)
                except Exception:  # pylint:disable=broad-except
                    await await_result(self.on_exception, request)
                    raise

                # If consecutive_challenge == True, this could be a third consecutive 401
                if response.http_response.status_code == 401 and not consecutive_challenge:
                    # If the previous challenge wasn't from CAE, we can try this function one more time
                    if not claims_challenge:
                        return await self.handle_challenge_flow(request, response, consecutive_challenge=True)
                await await_result(self.on_response, request, response)
        return response

    async def on_request(self, request: PipelineRequest) -> None:
        _enforce_tls(request)
        challenge = ChallengeCache.get_challenge_for_url(request.http_request.url)
        if challenge:
            # Note that if the vault has moved to a new tenant since our last request for it, this request will fail.
            if self._need_new_token():
                # azure-identity credentials require an AADv2 scope but the challenge may specify an AADv1 resource
                scope = challenge.get_scope() or challenge.get_resource() + "/.default"
                await self._request_kv_token(scope, challenge)

            bearer_token = cast(Union[AccessToken, AccessTokenInfo], self._token).token
            request.http_request.headers["Authorization"] = f"Bearer {bearer_token}"
            return

        # else: discover authentication information by eliciting a challenge from Key Vault. Remove any request data,
        # saving it for later. Key Vault will reject the request as unauthorized and respond with a challenge.
        # on_challenge will parse that challenge, use the original request including the body, authorize the
        # request, and tell super to send it again.
        if request.http_request.content:
            self._request_copy = request.http_request
            bodiless_request = HttpRequest(
                method=request.http_request.method,
                url=request.http_request.url,
                headers=deepcopy(request.http_request.headers),
            )
            bodiless_request.headers["Content-Length"] = "0"
            request.http_request = bodiless_request

    async def on_challenge(self, request: PipelineRequest, response: PipelineResponse) -> bool:
        try:
            # CAE challenges may not include a scope or tenant; cache from the previous challenge to use if necessary
            old_scope: Optional[str] = None
            old_tenant: Optional[str] = None
            cached_challenge = ChallengeCache.get_challenge_for_url(request.http_request.url)
            if cached_challenge:
                old_scope = cached_challenge.get_scope() or cached_challenge.get_resource() + "/.default"
                old_tenant = cached_challenge.tenant_id

            challenge = _update_challenge(request, response)
            # CAE challenges may not include a scope or tenant; use the previous challenge's values if necessary
            if challenge.claims and old_scope:
                challenge._parameters["scope"] = old_scope  # pylint:disable=protected-access
                challenge.tenant_id = old_tenant
            # azure-identity credentials require an AADv2 scope but the challenge may specify an AADv1 resource
            scope = challenge.get_scope() or challenge.get_resource() + "/.default"
        except ValueError:
            return False

        if self._verify_challenge_resource:
            resource_domain = urlparse(scope).netloc
            if not resource_domain:
                raise ValueError(f"The challenge contains invalid scope '{scope}'.")

            request_domain = urlparse(request.http_request.url).netloc
            if not request_domain.lower().endswith(f".{resource_domain.lower()}"):
                raise ValueError(
                    f"The challenge resource '{resource_domain}' does not match the requested domain. Pass "
                    "`verify_challenge_resource=False` to your client's constructor to disable this verification. "
                    "See https://aka.ms/azsdk/blog/vault-uri for more information."
                )

        # If we had created a request copy in on_request, use it now to send along the original body content
        if self._request_copy:
            request.http_request = self._request_copy

        # The tenant parsed from AD FS challenges is "adfs"; we don't actually need a tenant for AD FS authentication
        # For AD FS we skip cross-tenant authentication per https://github.com/Azure/azure-sdk-for-python/issues/28648
        if challenge.tenant_id and challenge.tenant_id.lower().endswith("adfs"):
            await self.authorize_request(request, scope, claims=challenge.claims)
        else:
            await self.authorize_request(request, scope, claims=challenge.claims, tenant_id=challenge.tenant_id)

        return True

    def _need_new_token(self) -> bool:
        now = time.time()
        refresh_on = getattr(self._token, "refresh_on", None)
        return not self._token or (refresh_on and refresh_on <= now) or self._token.expires_on - now < 300

    async def _request_kv_token(self, scope: str, challenge: HttpChallenge) -> None:
        """Implementation of BearerTokenCredentialPolicy's _request_token method, but specific to Key Vault.

        :param str scope: The scope for which to request a token.
        :param challenge: The challenge for the request being made.
        :type challenge: HttpChallenge
        """
        # Exclude tenant for AD FS authentication
        exclude_tenant = challenge.tenant_id and challenge.tenant_id.lower().endswith("adfs")
        # The AsyncSupportsTokenInfo protocol needs TokenRequestOptions for token requests instead of kwargs
        if hasattr(self._credential, "get_token_info"):
            options: TokenRequestOptions = {"enable_cae": True}
            if challenge.tenant_id and not exclude_tenant:
                options["tenant_id"] = challenge.tenant_id
            self._token = await cast(AsyncSupportsTokenInfo, self._credential).get_token_info(scope, options=options)
        else:
            if exclude_tenant:
                self._token = await self._credential.get_token(scope, enable_cae=True)
            else:
                self._token = await cast(AsyncTokenCredential, self._credential).get_token(
                    scope, tenant_id=challenge.tenant_id, enable_cae=True
                )
