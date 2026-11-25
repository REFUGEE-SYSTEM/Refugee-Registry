from datetime import date
from typing import Optional

from openg2p_registry_core.schemas import (
    G2PGeoHistorySchema,
    G2PGeoSchema,
    G2PIntakeFormSchemaBase,
    G2PRegisterBaseSchema,
    G2PRegisterHistorySchema,
)

from ..models.enums import LegalStatusEnum
from .geo_address_lines import G2PGeoAddressLinesSchema


class G2PSchemaHousehold:
    group_size: Optional[int] = None
    number_of_male: Optional[int] = None
    number_of_female: Optional[int] = None
    number_of_children: Optional[int] = None
    date_of_arrival: Optional[date] = None
    registration_date: Optional[date] = None
    legal_status: Optional[LegalStatusEnum] = None
    current_country_of_asylum_address: Optional[str] = None
    country_of_origin: Optional[str] = None
    phone_number: Optional[str] = None
    consent_or_prohibition_to_share_information: Optional[bool] = None


class G2PRegisterSchemaHousehold(
    G2PRegisterBaseSchema, G2PGeoSchema, G2PGeoAddressLinesSchema, G2PSchemaHousehold
):
    """Schema for Household register."""


class G2PRegisterHistorySchemaHousehold(
    G2PRegisterHistorySchema, G2PGeoHistorySchema, G2PSchemaHousehold
):
    """Schema for Household history."""


class G2PIntakeFormSchemaHousehold(
    G2PIntakeFormSchemaBase,
    G2PRegisterBaseSchema,
    G2PGeoSchema,
    G2PGeoAddressLinesSchema,
    G2PSchemaHousehold,
):
    """Schema for Household intake form."""
