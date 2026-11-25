from datetime import date
from typing import Optional

from openg2p_registry_core.schemas import (
    G2PIntakeFormSchemaBase,
    G2PRegisterBaseSchema,
    G2PRegisterHistorySchema,
)

from ..models.enums import RelativeRelationshipEnum


class G2PSchemaRelative:
    relationship: Optional[RelativeRelationshipEnum] = None
    full_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    location_or_status: Optional[str] = None


class G2PRegisterSchemaRelative(G2PRegisterBaseSchema, G2PSchemaRelative):
    """Schema for Relative register."""


class G2PRegisterHistorySchemaRelative(G2PRegisterHistorySchema, G2PSchemaRelative):
    """Schema for Relative history."""


class G2PIntakeFormSchemaRelative(
    G2PIntakeFormSchemaBase, G2PRegisterBaseSchema, G2PSchemaRelative
):
    """Schema for Relative intake form."""
