# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
import pytest
from azure.mgmt.apimanagement import ApiManagementClient

from devtools_testutils import AzureMgmtRecordedTestCase, RandomNameResourceGroupPreparer, recorded_by_proxy

AZURE_LOCATION = "eastus"


@pytest.mark.skip("you may need to update the auto-generated test case before run it")
class TestApiManagementPortalRevisionOperations(AzureMgmtRecordedTestCase):
    def setup_method(self, method):
        self.client = self.create_mgmt_client(ApiManagementClient)

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_portal_revision_list_by_service(self, resource_group):
        response = self.client.portal_revision.list_by_service(
            resource_group_name=resource_group.name,
            service_name="str",
            api_version="2024-05-01",
        )
        result = [r for r in response]
        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_portal_revision_get_entity_tag(self, resource_group):
        response = self.client.portal_revision.get_entity_tag(
            resource_group_name=resource_group.name,
            service_name="str",
            portal_revision_id="str",
            api_version="2024-05-01",
        )

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_portal_revision_get(self, resource_group):
        response = self.client.portal_revision.get(
            resource_group_name=resource_group.name,
            service_name="str",
            portal_revision_id="str",
            api_version="2024-05-01",
        )

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_portal_revision_begin_create_or_update(self, resource_group):
        response = self.client.portal_revision.begin_create_or_update(
            resource_group_name=resource_group.name,
            service_name="str",
            portal_revision_id="str",
            parameters={
                "createdDateTime": "2020-02-20 00:00:00",
                "description": "str",
                "id": "str",
                "isCurrent": bool,
                "name": "str",
                "provisioningState": "str",
                "status": "str",
                "statusDetails": "str",
                "type": "str",
                "updatedDateTime": "2020-02-20 00:00:00",
            },
            api_version="2024-05-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_portal_revision_begin_update(self, resource_group):
        response = self.client.portal_revision.begin_update(
            resource_group_name=resource_group.name,
            service_name="str",
            portal_revision_id="str",
            if_match="str",
            parameters={
                "createdDateTime": "2020-02-20 00:00:00",
                "description": "str",
                "id": "str",
                "isCurrent": bool,
                "name": "str",
                "provisioningState": "str",
                "status": "str",
                "statusDetails": "str",
                "type": "str",
                "updatedDateTime": "2020-02-20 00:00:00",
            },
            api_version="2024-05-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...
