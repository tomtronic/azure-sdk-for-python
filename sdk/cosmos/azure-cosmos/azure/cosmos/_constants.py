# The MIT License (MIT)
# Copyright (c) 2014 Microsoft Corporation

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Class for defining internal constants in the Azure Cosmos database service.
"""


from typing import Dict
from typing_extensions import Literal


class _Constants:
    """Constants used in the azure-cosmos package"""

    UserConsistencyPolicy: Literal["userConsistencyPolicy"] = "userConsistencyPolicy"
    DefaultConsistencyLevel: Literal["defaultConsistencyLevel"] = "defaultConsistencyLevel"

    # GlobalDB related constants
    WritableLocations: Literal["writableLocations"] = "writableLocations"
    ReadableLocations: Literal["readableLocations"] = "readableLocations"
    Name: Literal["name"] = "name"
    DatabaseAccountEndpoint: Literal["databaseAccountEndpoint"] = "databaseAccountEndpoint"
    DefaultEndpointsRefreshTime: int = 5 * 60 * 1000 # milliseconds
    UnavailableEndpointDBATimeouts: int = 1 # seconds

    # ServiceDocument Resource
    EnableMultipleWritableLocations: Literal["enableMultipleWriteLocations"] = "enableMultipleWriteLocations"

    # Environment variables
    NON_STREAMING_ORDER_BY_DISABLED_CONFIG: str = "AZURE_COSMOS_DISABLE_NON_STREAMING_ORDER_BY"
    NON_STREAMING_ORDER_BY_DISABLED_CONFIG_DEFAULT: str = "False"
    HS_MAX_ITEMS_CONFIG: str = "AZURE_COSMOS_HYBRID_SEARCH_MAX_ITEMS"
    HS_MAX_ITEMS_CONFIG_DEFAULT: int = 1000
    MAX_ITEM_BUFFER_VS_CONFIG: str = "AZURE_COSMOS_MAX_ITEM_BUFFER_VECTOR_SEARCH"
    MAX_ITEM_BUFFER_VS_CONFIG_DEFAULT: int = 50000

    # Application region related constants
    LATENCY_PROBE_COUNT: int = 3 # Number of probes to send to each region
    LATENCY_PROBE_TIMEOUT_SEC: float = 0.5 # Timeout for a single probe (seconds)
    LATENCY_PROBE_TOTAL_TIMEOUT_SEC: float = 1.5 # Total timeout for all probes to all regions (seconds)
    LATENCY_PROBE_MAX_WORKERS: int = 9 # Maximum number of concurrent workers for latency probes    

    # Error code translations
    ERROR_TRANSLATIONS: Dict[int, str] = {
        400: "BAD_REQUEST - Request being sent is invalid.",
        401: "UNAUTHORIZED - The input authorization token can't serve the request.",
        403: "FORBIDDEN",
        404: "NOT_FOUND - Entity with the specified id does not exist in the system.",
        405: "METHOD_NOT_ALLOWED",
        408: "REQUEST_TIMEOUT",
        409: "CONFLICT - Entity with the specified id already exists in the system.",
        410: "GONE",
        412: "PRECONDITION_FAILED - Operation cannot be performed because one of the specified precondition is not met",
        413: "REQUEST_ENTITY_TOO_LARGE - Document size exceeds limit.",
        424: "FAILED_DEPENDENCY - There is a failure in the transactional batch.",
        429: "TOO_MANY_REQUESTS",
        449: "RETRY_WITH - Conflicting request to resource has been attempted. Retry to avoid conflicts."
    }
