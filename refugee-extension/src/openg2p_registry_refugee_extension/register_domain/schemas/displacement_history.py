from datetime import date
from typing import Optional

from openg2p_registry_core.schemas import (
    G2PIntakeFormSchemaBase,
    G2PRegisterBaseSchema,
    G2PRegisterHistorySchema,
)


class G2PSchemaDisplacementHistory:
    reasons_for_unwillingness_or_inability_to_return: Optional[str] = None
    travel_details: Optional[str] = None
    departure_date: Optional[date] = None
    transit_countries: Optional[str] = None


class G2PRegisterSchemaDisplacementHistory(
    G2PRegisterBaseSchema, G2PSchemaDisplacementHistory
):
    """Schema for DisplacementHistory register."""


class G2PRegisterHistorySchemaDisplacementHistory(
    G2PRegisterHistorySchema, G2PSchemaDisplacementHistory
):
    """Schema for DisplacementHistory history."""


class G2PIntakeFormSchemaDisplacementHistory(
    G2PIntakeFormSchemaBase, G2PRegisterBaseSchema, G2PSchemaDisplacementHistory
):
    """Schema for DisplacementHistory intake form."""
