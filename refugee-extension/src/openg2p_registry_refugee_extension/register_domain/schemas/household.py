from datetime import date, datetime
from typing import Optional

from openg2p_registry_core.schemas import (
    G2PGeoHistorySchema,
    G2PGeoSchema,
    G2PIntakeFormSchemaBase,
    G2PRegisterBaseSchema,
    G2PRegisterHistorySchema,
)

from ..models.enums import (
    DeliveryMechanismEnum,
    DeliveryModalityEnum,
    ExitReasonEnum,
    IncomeSourceEnum,
    LegalStatusEnum,
    PaymentStatusEnum,
    RefugeeRecordStatusEnum,
)
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

    entry_point: Optional[str] = None
    registration_site: Optional[str] = None
    registering_officer_id: Optional[str] = None
    head_of_household_id: Optional[str] = None
    dependency_ratio: Optional[float] = None
    is_female_headed: Optional[bool] = None
    is_child_headed: Optional[bool] = None
    host_district: Optional[str] = None
    settlement_location: Optional[str] = None
    zone_cluster: Optional[str] = None
    village_block: Optional[str] = None
    main_income_source: Optional[IncomeSourceEnum] = None
    working_age_earners: Optional[int] = None
    assistance_category: Optional[str] = None
    vulnerability_score: Optional[int] = None
    is_new_arrival: Optional[bool] = None
    new_arrival_end_date: Optional[date] = None
    programmes_enrolled: Optional[list[str]] = None
    enrolment_date: Optional[date] = None
    exit_date: Optional[date] = None
    exit_reason: Optional[ExitReasonEnum] = None
    delivery_modality: Optional[DeliveryModalityEnum] = None
    delivery_mechanism: Optional[DeliveryMechanismEnum] = None
    primary_recipient_id: Optional[str] = None
    food_distribution_point: Optional[str] = None
    entitlement_amount: Optional[float] = None
    entitlement_currency: Optional[str] = None
    payment_cycle: Optional[str] = None
    payment_status: Optional[PaymentStatusEnum] = None
    transaction_reference: Optional[str] = None
    transaction_date: Optional[date] = None
    lifecycle_status: Optional[RefugeeRecordStatusEnum] = None
    last_updated_at: Optional[datetime] = None
    last_updated_by: Optional[str] = None


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
