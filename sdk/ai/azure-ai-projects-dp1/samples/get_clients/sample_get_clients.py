# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

"""
DESCRIPTION:
    Given an AIProjectClient, this sample demonstrates how to use the synchronous `get_client` method
    to get an authenticated 
    - `AssistantClient` (from the azure-ai-assistant package).
    - `ChatCompletionsClient`, `EmbeddingsClient` and `ImageEmbeddingsClient` (from the azure-ai-inference package).
    - `AzureOpenAI` client (from the openai package).

USAGE:
    python sample_get_client.py

    Before running the sample:

    pip install azure-ai-projects azure-identity

    Set these environment variables with your own values:
    1) PROJECT_ENDPOINT - Required. The Azure AI Project endpoint, as found in the overview page of your
       Azure AI Foundry project.
    2) CONNECTION_NAME - The name of a connection, as found in the "Connected resources" tab
       in the Management Center of your AI Foundry project.
"""

import os
from azure.ai.projects.dp1 import AIProjectClient
from azure.ai.projects.dp1.models import ClientType
from azure.identity import DefaultAzureCredential

endpoint = os.environ["PROJECT_ENDPOINT"]
#connection_name = os.environ["CONNECTION_NAME"]

with AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(),
) as project_client:

    print("Get an authenticated AssistantClient")
    assistant_client = project_client.get_client(ClientType.Assistant)


