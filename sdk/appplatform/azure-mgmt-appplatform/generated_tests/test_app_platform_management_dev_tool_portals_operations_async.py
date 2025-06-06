# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
import pytest
from azure.mgmt.appplatform.aio import AppPlatformManagementClient

from devtools_testutils import AzureMgmtRecordedTestCase, RandomNameResourceGroupPreparer
from devtools_testutils.aio import recorded_by_proxy_async

AZURE_LOCATION = "eastus"


@pytest.mark.skip("you may need to update the auto-generated test case before run it")
class TestAppPlatformManagementDevToolPortalsOperationsAsync(AzureMgmtRecordedTestCase):
    def setup_method(self, method):
        self.client = self.create_mgmt_client(AppPlatformManagementClient, is_async=True)

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_list(self, resource_group):
        response = self.client.dev_tool_portals.list(
            resource_group_name=resource_group.name,
            service_name="str",
            api_version="2023-12-01",
        )
        result = [r async for r in response]
        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_get(self, resource_group):
        response = await self.client.dev_tool_portals.get(
            resource_group_name=resource_group.name,
            service_name="str",
            dev_tool_portal_name="str",
            api_version="2023-12-01",
        )

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_begin_create_or_update(self, resource_group):
        response = await (
            await self.client.dev_tool_portals.begin_create_or_update(
                resource_group_name=resource_group.name,
                service_name="str",
                dev_tool_portal_name="str",
                dev_tool_portal_resource={
                    "id": "str",
                    "name": "str",
                    "properties": {
                        "components": [
                            {
                                "instances": [{"name": "str", "status": "str"}],
                                "name": "str",
                                "resourceRequests": {"cpu": "str", "instanceCount": 0, "memory": "str"},
                            }
                        ],
                        "features": {
                            "applicationAccelerator": {"route": "str", "state": "Enabled"},
                            "applicationLiveView": {"route": "str", "state": "Enabled"},
                        },
                        "provisioningState": "str",
                        "public": False,
                        "ssoProperties": {
                            "clientId": "str",
                            "clientSecret": "str",
                            "metadataUrl": "str",
                            "scopes": ["str"],
                        },
                        "url": "str",
                    },
                    "systemData": {
                        "createdAt": "2020-02-20 00:00:00",
                        "createdBy": "str",
                        "createdByType": "str",
                        "lastModifiedAt": "2020-02-20 00:00:00",
                        "lastModifiedBy": "str",
                        "lastModifiedByType": "str",
                    },
                    "type": "str",
                },
                api_version="2023-12-01",
            )
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_begin_delete(self, resource_group):
        response = await (
            await self.client.dev_tool_portals.begin_delete(
                resource_group_name=resource_group.name,
                service_name="str",
                dev_tool_portal_name="str",
                api_version="2023-12-01",
            )
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...
