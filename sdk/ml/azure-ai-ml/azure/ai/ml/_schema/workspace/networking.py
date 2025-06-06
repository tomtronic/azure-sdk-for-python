# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

# pylint: disable=unused-argument,no-else-return

from marshmallow import EXCLUDE, fields
from marshmallow.decorators import post_load, pre_dump

from azure.ai.ml._schema import ExperimentalField
from azure.ai.ml._schema.core.fields import NestedField, StringTransformedEnum, UnionField
from azure.ai.ml._schema.core.schema_meta import PatchedSchemaMeta
from azure.ai.ml._utils.utils import _snake_to_camel, camel_to_snake
from azure.ai.ml.constants._workspace import FirewallSku, IsolationMode, OutboundRuleCategory
from azure.ai.ml.entities._workspace.networking import (
    FqdnDestination,
    ManagedNetwork,
    PrivateEndpointDestination,
    ServiceTagDestination,
)


class ManagedNetworkStatusSchema(metaclass=PatchedSchemaMeta):
    spark_ready = fields.Bool(dump_only=True)
    status = fields.Str(dump_only=True)


class FqdnOutboundRuleSchema(metaclass=PatchedSchemaMeta):
    name = fields.Str(required=True)
    parent_rule_names = fields.List(fields.Str(), dump_only=True)
    type = fields.Constant("fqdn")
    destination = fields.Str(required=True)
    category = StringTransformedEnum(
        allowed_values=[
            OutboundRuleCategory.REQUIRED,
            OutboundRuleCategory.RECOMMENDED,
            OutboundRuleCategory.USER_DEFINED,
        ],
        casing_transform=camel_to_snake,
        metadata={"description": "outbound rule category."},
        dump_only=True,
    )
    status = fields.Str(dump_only=True)

    @post_load
    def createdestobject(self, data, **kwargs):
        dest = data.get("destination")
        category = data.get("category", OutboundRuleCategory.USER_DEFINED)
        name = data.get("name")
        status = data.get("status", None)
        return FqdnDestination(
            name=name,
            destination=dest,
            category=_snake_to_camel(category),
            status=status,
        )


class ServiceTagDestinationSchema(metaclass=PatchedSchemaMeta):
    service_tag = fields.Str(required=True)
    protocol = fields.Str(required=True)
    port_ranges = fields.Str(required=True)
    address_prefixes = fields.List(fields.Str())


class ServiceTagOutboundRuleSchema(metaclass=PatchedSchemaMeta):
    name = fields.Str(required=True)
    parent_rule_names = fields.List(fields.Str(), dump_only=True)
    type = fields.Constant("service_tag")
    destination = NestedField(ServiceTagDestinationSchema, required=True)
    category = StringTransformedEnum(
        allowed_values=[
            OutboundRuleCategory.REQUIRED,
            OutboundRuleCategory.RECOMMENDED,
            OutboundRuleCategory.USER_DEFINED,
        ],
        casing_transform=camel_to_snake,
        metadata={"description": "outbound rule category."},
        dump_only=True,
    )
    status = fields.Str(dump_only=True)

    @pre_dump
    def predump(self, data, **kwargs):
        data.destination = self.service_tag_dest2dict(
            data.service_tag, data.protocol, data.port_ranges, data.address_prefixes
        )
        return data

    @post_load
    def createdestobject(self, data, **kwargs):
        dest = data.get("destination")
        category = data.get("category", OutboundRuleCategory.USER_DEFINED)
        name = data.get("name")
        status = data.get("status", None)
        return ServiceTagDestination(
            name=name,
            service_tag=dest["service_tag"],
            protocol=dest["protocol"],
            port_ranges=dest["port_ranges"],
            address_prefixes=dest.get("address_prefixes", None),
            category=_snake_to_camel(category),
            status=status,
        )

    def service_tag_dest2dict(self, service_tag, protocol, port_ranges, address_prefixes):
        service_tag_dest = {}
        service_tag_dest["service_tag"] = service_tag
        service_tag_dest["protocol"] = protocol
        service_tag_dest["port_ranges"] = port_ranges
        service_tag_dest["address_prefixes"] = address_prefixes
        return service_tag_dest


class PrivateEndpointDestinationSchema(metaclass=PatchedSchemaMeta):
    service_resource_id = fields.Str(required=True)
    subresource_target = fields.Str(required=True)
    spark_enabled = fields.Bool(required=True)


class PrivateEndpointOutboundRuleSchema(metaclass=PatchedSchemaMeta):
    name = fields.Str(required=True)
    parent_rule_names = fields.List(fields.Str(), dump_only=True)
    type = fields.Constant("private_endpoint")
    destination = NestedField(PrivateEndpointDestinationSchema, required=True)
    fqdns = fields.List(fields.Str())
    category = StringTransformedEnum(
        allowed_values=[
            OutboundRuleCategory.REQUIRED,
            OutboundRuleCategory.RECOMMENDED,
            OutboundRuleCategory.USER_DEFINED,
            OutboundRuleCategory.DEPENDENCY,
        ],
        casing_transform=camel_to_snake,
        metadata={"description": "outbound rule category."},
        dump_only=True,
    )
    status = fields.Str(dump_only=True)

    @pre_dump
    def predump(self, data, **kwargs):
        data.destination = self.pe_dest2dict(data.service_resource_id, data.subresource_target, data.spark_enabled)
        return data

    @post_load
    def createdestobject(self, data, **kwargs):
        dest = data.get("destination")
        category = data.get("category", OutboundRuleCategory.USER_DEFINED)
        name = data.get("name")
        status = data.get("status", None)
        fqdns = data.get("fqdns", None)
        return PrivateEndpointDestination(
            name=name,
            service_resource_id=dest["service_resource_id"],
            subresource_target=dest["subresource_target"],
            spark_enabled=dest["spark_enabled"],
            category=_snake_to_camel(category),
            status=status,
            fqdns=fqdns,
        )

    def pe_dest2dict(self, service_resource_id, subresource_target, spark_enabled):
        pedest = {}
        pedest["service_resource_id"] = service_resource_id
        pedest["subresource_target"] = subresource_target
        pedest["spark_enabled"] = spark_enabled
        return pedest


class ManagedNetworkSchema(metaclass=PatchedSchemaMeta):
    isolation_mode = StringTransformedEnum(
        allowed_values=[
            IsolationMode.DISABLED,
            IsolationMode.ALLOW_INTERNET_OUTBOUND,
            IsolationMode.ALLOW_ONLY_APPROVED_OUTBOUND,
        ],
        casing_transform=camel_to_snake,
        metadata={"description": "isolation mode for the workspace managed network."},
    )
    outbound_rules = fields.List(
        UnionField(
            [
                NestedField(PrivateEndpointOutboundRuleSchema, allow_none=False, unknown=EXCLUDE),
                NestedField(ServiceTagOutboundRuleSchema, allow_none=False, unknown=EXCLUDE),
                NestedField(
                    FqdnOutboundRuleSchema, allow_none=False, unknown=EXCLUDE
                ),  # this needs to be last since otherwise union field with match destination as a string
            ],
            allow_none=False,
            is_strict=True,
        ),
        allow_none=True,
    )
    firewall_sku = ExperimentalField(
        StringTransformedEnum(
            allowed_values=[
                FirewallSku.STANDARD,
                FirewallSku.BASIC,
            ],
            casing_transform=camel_to_snake,
            metadata={"description": "Firewall sku for FQDN rules in AllowOnlyApprovedOutbound mode"},
        )
    )
    network_id = fields.Str(required=False, dump_only=True)
    status = NestedField(ManagedNetworkStatusSchema, allow_none=False, unknown=EXCLUDE)

    @post_load
    def make(self, data, **kwargs):
        outbound_rules = data.get("outbound_rules", False)

        firewall_sku = data.get("firewall_sku", False)
        firewall_sku_value = _snake_to_camel(data["firewall_sku"]) if firewall_sku else FirewallSku.STANDARD

        if outbound_rules:
            return ManagedNetwork(
                isolation_mode=_snake_to_camel(data["isolation_mode"]),
                outbound_rules=outbound_rules,
                firewall_sku=firewall_sku_value,
            )
        else:
            return ManagedNetwork(
                isolation_mode=_snake_to_camel(data["isolation_mode"]),
                firewall_sku=firewall_sku_value,
            )
