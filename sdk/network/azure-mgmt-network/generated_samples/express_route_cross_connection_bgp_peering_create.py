# pylint: disable=line-too-long,useless-suppression
# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from azure.identity import DefaultAzureCredential

from azure.mgmt.network import NetworkManagementClient

"""
# PREREQUISITES
    pip install azure-identity
    pip install azure-mgmt-network
# USAGE
    python express_route_cross_connection_bgp_peering_create.py

    Before run the sample, please set the values of the client ID, tenant ID and client secret
    of the AAD application as environment variables: AZURE_CLIENT_ID, AZURE_TENANT_ID,
    AZURE_CLIENT_SECRET. For more info about how to get the value, please see:
    https://docs.microsoft.com/azure/active-directory/develop/howto-create-service-principal-portal
"""


def main():
    client = NetworkManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id="subid",
    )

    response = client.express_route_cross_connection_peerings.begin_create_or_update(
        resource_group_name="CrossConnection-SiliconValley",
        cross_connection_name="<circuitServiceKey>",
        peering_name="AzurePrivatePeering",
        peering_parameters={
            "properties": {
                "ipv6PeeringConfig": {
                    "primaryPeerAddressPrefix": "3FFE:FFFF:0:CD30::/126",
                    "secondaryPeerAddressPrefix": "3FFE:FFFF:0:CD30::4/126",
                },
                "peerASN": 200,
                "primaryPeerAddressPrefix": "192.168.16.252/30",
                "secondaryPeerAddressPrefix": "192.168.18.252/30",
                "vlanId": 200,
            }
        },
    ).result()
    print(response)


# x-ms-original-file: specification/network/resource-manager/Microsoft.Network/stable/2024-07-01/examples/ExpressRouteCrossConnectionBgpPeeringCreate.json
if __name__ == "__main__":
    main()
