from datetime import date
from typing import Optional

from openg2p_registry_core.schemas import (
    G2PIntakeFormSchemaBase,
    G2PRegisterBaseSchema,
    G2PRegisterHistorySchema,
)

from ..models.enums import NeedCategoryEnum, NeedSeverityEnum


class G2PSchemaSpecificNeeds:
    need_category: Optional[NeedCategoryEnum] = None
    severity: Optional[NeedSeverityEnum] = None
    date_identified: Optional[date] = None
    support_required: Optional[str] = None
    notes: Optional[str] = None


class G2PRegisterSchemaSpecificNeeds(G2PRegisterBaseSchema, G2PSchemaSpecificNeeds):
    """Schema for SpecificNeeds register."""


class G2PRegisterHistorySchemaSpecificNeeds(
    G2PRegisterHistorySchema, G2PSchemaSpecificNeeds
):
    """Schema for SpecificNeeds history."""


class G2PIntakeFormSchemaSpecificNeeds(
    G2PIntakeFormSchemaBase, G2PRegisterBaseSchema, G2PSchemaSpecificNeeds
):
    """Schema for SpecificNeeds intake form."""
