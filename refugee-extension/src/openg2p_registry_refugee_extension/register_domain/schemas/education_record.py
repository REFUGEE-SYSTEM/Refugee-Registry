from typing import Optional

from openg2p_registry_core.schemas import (
    G2PIntakeFormSchemaBase,
    G2PRegisterBaseSchema,
    G2PRegisterHistorySchema,
)

from ..models.enums import HighestEducationLevelEnum


class G2PSchemaEducationRecord:
    level: Optional[HighestEducationLevelEnum] = None
    institution: Optional[str] = None
    field_of_study: Optional[str] = None
    year_completed: Optional[int] = None


class G2PRegisterSchemaEducationRecord(G2PRegisterBaseSchema, G2PSchemaEducationRecord):
    """Schema for EducationRecord register."""


class G2PRegisterHistorySchemaEducationRecord(
    G2PRegisterHistorySchema, G2PSchemaEducationRecord
):
    """Schema for EducationRecord history."""


class G2PIntakeFormSchemaEducationRecord(
    G2PIntakeFormSchemaBase, G2PRegisterBaseSchema, G2PSchemaEducationRecord
):
    """Schema for EducationRecord intake form."""
