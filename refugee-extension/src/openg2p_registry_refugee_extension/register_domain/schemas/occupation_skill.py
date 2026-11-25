from typing import Optional

from openg2p_registry_core.schemas import (
    G2PIntakeFormSchemaBase,
    G2PRegisterBaseSchema,
    G2PRegisterHistorySchema,
)


class G2PSchemaOccupationSkill:
    occupation: Optional[str] = None
    skill: Optional[str] = None
    years_of_experience: Optional[int] = None


class G2PRegisterSchemaOccupationSkill(G2PRegisterBaseSchema, G2PSchemaOccupationSkill):
    """Schema for OccupationSkill register."""


class G2PRegisterHistorySchemaOccupationSkill(
    G2PRegisterHistorySchema, G2PSchemaOccupationSkill
):
    """Schema for OccupationSkill history."""


class G2PIntakeFormSchemaOccupationSkill(
    G2PIntakeFormSchemaBase, G2PRegisterBaseSchema, G2PSchemaOccupationSkill
):
    """Schema for OccupationSkill intake form."""
