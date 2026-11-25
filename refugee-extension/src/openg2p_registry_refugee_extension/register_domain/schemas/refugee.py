from datetime import date, datetime
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

from ..models.enums import (
    AuthResultEnum,
    DuplicateCheckEnum,
    ExitReasonEnum,
    HighestEducationLevelEnum,
    LegalStatusEnum,
    PresenceStatusEnum,
    RefugeeRecordStatusEnum,
    RelationshipToGroupEnum,
    ReligionEnum,
    SecurityScreeningEnum,
    UnaccompaniedChildEnum,
    WashingtonGroupAnswerEnum,
)
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

    arrival_date: Optional[date] = None
    is_birth_date_estimated: Optional[bool] = None
    nationality: Optional[str] = None
    legal_status: Optional[LegalStatusEnum] = None
    rsd_application_date: Optional[date] = None
    security_screening_status: Optional[SecurityScreeningEnum] = None
    presence_status: Optional[PresenceStatusEnum] = None
    unaccompanied_separated_status: Optional[UnaccompaniedChildEnum] = None
    wg_seeing: Optional[WashingtonGroupAnswerEnum] = None
    wg_hearing: Optional[WashingtonGroupAnswerEnum] = None
    wg_walking: Optional[WashingtonGroupAnswerEnum] = None
    wg_remembering: Optional[WashingtonGroupAnswerEnum] = None
    wg_self_care: Optional[WashingtonGroupAnswerEnum] = None
    wg_communicating: Optional[WashingtonGroupAnswerEnum] = None
    has_serious_medical_condition: Optional[bool] = None
    programmes_enrolled: Optional[list[str]] = None
    enrolment_date: Optional[date] = None
    exit_date: Optional[date] = None
    exit_reason: Optional[ExitReasonEnum] = None
    auth_result: Optional[AuthResultEnum] = None
    informed_consent_given: Optional[bool] = None
    informed_consent_date: Optional[date] = None
    partner_data_sharing_consent: Optional[list[str]] = None
    lifecycle_status: Optional[RefugeeRecordStatusEnum] = None
    duplicate_check_result: Optional[DuplicateCheckEnum] = None
    last_updated_at: Optional[datetime] = None
    last_updated_by: Optional[str] = None


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
