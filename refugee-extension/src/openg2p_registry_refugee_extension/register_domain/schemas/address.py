from typing import Optional

from openg2p_registry_core.schemas import (
    G2PIntakeFormSchemaBase,
    G2PRegisterBaseSchema,
    G2PRegisterHistorySchema,
)

from ..models.enums import AddressTypeEnum


class G2PSchemaAddress:
    address_type: Optional[AddressTypeEnum] = None
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    country: Optional[str] = None


class G2PRegisterSchemaAddress(G2PRegisterBaseSchema, G2PSchemaAddress):
    """Schema for Address register."""


class G2PRegisterHistorySchemaAddress(G2PRegisterHistorySchema, G2PSchemaAddress):
    """Schema for Address history."""


class G2PIntakeFormSchemaAddress(
    G2PIntakeFormSchemaBase, G2PRegisterBaseSchema, G2PSchemaAddress
):
    """Schema for Address intake form."""
