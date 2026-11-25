from typing import Optional

from openg2p_registry_core.schemas import (
    G2PGeoHistorySchema,
    G2PGeoSchema,
    G2PIntakeFormSchemaBase,
    G2PPersonHistorySchema,
    G2PPersonSchema,
    G2PRegisterBaseSchema,
    G2PRegisterHistorySchema,
)

from ..models.enums import HighestEducationLevelEnum, RelationshipToGroupEnum, ReligionEnum
from .geo_address_lines import G2PGeoAddressLinesSchema


class G2PSchemaRefugee:
    relationship_to_group: Optional[RelationshipToGroupEnum] = None
    country_of_origin: Optional[str] = None
    fathers_name: Optional[str] = None
    mothers_name: Optional[str] = None
    highest_education_level: Optional[HighestEducationLevelEnum] = None
    last_occupation: Optional[str] = None
    religion: Optional[ReligionEnum] = None
    languages_known: Optional[list[str]] = None
    place_of_birth: Optional[str] = None


class G2PRegisterSchemaRefugee(
    G2PRegisterBaseSchema,
    G2PPersonSchema,
    G2PGeoSchema,
    G2PGeoAddressLinesSchema,
    G2PSchemaRefugee,
):
    """Schema for Refugee register."""


class G2PRegisterHistorySchemaRefugee(
    G2PRegisterHistorySchema, G2PPersonHistorySchema, G2PGeoHistorySchema, G2PSchemaRefugee
):
    """Schema for Refugee history."""


class G2PIntakeFormSchemaRefugee(
    G2PIntakeFormSchemaBase,
    G2PRegisterBaseSchema,
    G2PPersonSchema,
    G2PGeoSchema,
    G2PGeoAddressLinesSchema,
    G2PSchemaRefugee,
):
    """Schema for Refugee intake form."""
