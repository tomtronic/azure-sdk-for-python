# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""Customize generated code here.

Follow our quickstart for examples: https://aka.ms/azsdk/python/dpcodegen/python/customize
"""
from typing import List
from enum import Enum
from azure.core import CaseInsensitiveEnumMeta

class ClientType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The type of client library used in the get_client method."""

    CHAT_COMPLETIONS_CLIENT = "ChatCompletionsClient"
    """ChatCompletionsClient from the azure-ai-inference package"""

    EMBEDDINGS_CLIENT = "EmbeddingsClient"
    """EmbeddingsClient from the azure-ai-inference package"""

    IMAGE_EMBEDDINGS_CLIENT = "ImageEmbeddingsClient"
    """ImageEmbeddingsClient from the azure-ai-inference package"""

    AZURE_OPEN_AI = "AzureOpenAI"
    """AzureOpenAI client from the openai package"""

__all__: List[str] = [
    "ClientType"
]  # Add all objects you want publicly available to users at this package level

def patch_sdk():
    """Do not remove from this file.

    `patch_sdk` is a last resort escape hatch that allows you to do customizations
    you can't accomplish using the techniques described in
    https://aka.ms/azsdk/python/dpcodegen/python/customize
    """
