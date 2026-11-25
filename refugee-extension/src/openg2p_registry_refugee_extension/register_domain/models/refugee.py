from datetime import date, datetime, timezone

from openg2p_registry_core.models import (
    G2PGeo,
    G2PGeoHistory,
    G2PPerson,
    G2PPersonHistory,
    G2PRegister,
    G2PRegisterHistory,
)
from openg2p_registry_core.models.g2p_intake_form import G2PIntakeForm
from sqlalchemy import Boolean, Date, DateTime, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, validates

from ..services import G2PRegisterDomainServiceRefugee
from .enums import (
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

# TODO: Biometrics (C01 facial photo, C02 fingerprints, C05 last biometric verification date)
# are out of scope for this demo build and deferred to a separate integration step.


class G2PRefugee:
    """Domain attributes for Refugee individual (Uganda mandatory model + preserved legacy columns)."""

    # Legacy columns (preserved, never dropped)
    relationship_to_group: Mapped[RelationshipToGroupEnum] = mapped_column(
        String, nullable=True
    )  # F02
    country_of_origin: Mapped[str] = mapped_column(String, nullable=True)  # B08
    fathers_name: Mapped[str] = mapped_column(String, nullable=True)
    mothers_name: Mapped[str] = mapped_column(String, nullable=True)
    highest_education_level: Mapped[HighestEducationLevelEnum] = mapped_column(
        String, nullable=True
    )
    last_occupation: Mapped[str] = mapped_column(String, nullable=True)
    religion: Mapped[ReligionEnum] = mapped_column(String, nullable=True)
    languages_known: Mapped[list] = mapped_column(JSONB, nullable=True)  # B11
    place_of_birth: Mapped[str] = mapped_column(String, nullable=True)  # B07

    # Uganda Mandatory Individual attributes
    arrival_date: Mapped[date] = mapped_column(Date, nullable=True)  # A03
    is_birth_date_estimated: Mapped[bool] = mapped_column(Boolean, nullable=True)  # B06
    nationality: Mapped[str] = mapped_column(String, nullable=True)  # B09
    legal_status: Mapped[LegalStatusEnum] = mapped_column(String, nullable=True)  # E01
    rsd_application_date: Mapped[date] = mapped_column(Date, nullable=True)  # E03
    security_screening_status: Mapped[SecurityScreeningEnum] = mapped_column(
        String, nullable=True
    )  # E07
    presence_status: Mapped[PresenceStatusEnum] = mapped_column(String, nullable=True)  # F07
    unaccompanied_separated_status: Mapped[UnaccompaniedChildEnum] = mapped_column(
        String, nullable=True
    )  # I02
    wg_seeing: Mapped[WashingtonGroupAnswerEnum] = mapped_column(String, nullable=True)  # J01
    wg_hearing: Mapped[WashingtonGroupAnswerEnum] = mapped_column(String, nullable=True)  # J01
    wg_walking: Mapped[WashingtonGroupAnswerEnum] = mapped_column(String, nullable=True)  # J01
    wg_remembering: Mapped[WashingtonGroupAnswerEnum] = mapped_column(String, nullable=True)  # J01
    wg_self_care: Mapped[WashingtonGroupAnswerEnum] = mapped_column(String, nullable=True)  # J01
    wg_communicating: Mapped[WashingtonGroupAnswerEnum] = mapped_column(String, nullable=True)  # J01
    has_serious_medical_condition: Mapped[bool] = mapped_column(Boolean, nullable=True)  # J02
    programmes_enrolled: Mapped[list] = mapped_column(JSONB, nullable=True)  # M04
    enrolment_date: Mapped[date] = mapped_column(Date, nullable=True)  # M05
    exit_date: Mapped[date] = mapped_column(Date, nullable=True)  # M05
    exit_reason: Mapped[ExitReasonEnum] = mapped_column(String, nullable=True)  # M05
    auth_result: Mapped[AuthResultEnum] = mapped_column(String, nullable=True)  # O02
    informed_consent_given: Mapped[bool] = mapped_column(Boolean, nullable=True)  # P01
    informed_consent_date: Mapped[date] = mapped_column(Date, nullable=True)  # P01
    partner_data_sharing_consent: Mapped[list] = mapped_column(JSONB, nullable=True)  # P02
    lifecycle_status: Mapped[RefugeeRecordStatusEnum] = mapped_column(String, nullable=True)  # Q01
    duplicate_check_result: Mapped[DuplicateCheckEnum] = mapped_column(String, nullable=True)  # Q03
    last_updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)  # Q04
    last_updated_by: Mapped[str] = mapped_column(String, nullable=True)  # Q04

    @validates("last_updated_at")
    def _coerce_last_updated_at(self, _key, value):
        if value is None or value == "":
            return datetime.now(timezone.utc).replace(tzinfo=None)
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace("Z", "+00:00")).replace(tzinfo=None)
        return value


class G2PRegisterRefugee(G2PRegister, G2PPerson, G2PGeo, G2PRefugee):
    __tablename__ = "g2p_register_refugees"

    def get_record_name_fields(self) -> str:
        """Return refugee fields used to build record_name."""
        return G2PRegisterDomainServiceRefugee().construct_record_name(self.to_dict())

    def get_search_text_fields(self) -> str:
        """Return refugee fields used to build search_text."""
        return G2PRegisterDomainServiceRefugee().construct_search_text(self.to_dict())


class G2PRegisterHistoryRefugee(
    G2PRegisterHistory, G2PPersonHistory, G2PGeoHistory, G2PRefugee
):
    __tablename__ = "g2p_register_history_refugees"


class G2PIntakeFormRefugee(
    G2PIntakeForm, G2PRegister, G2PPerson, G2PGeo, G2PRefugee
):
    __tablename__ = "g2p_intake_form_refugees"

    def get_record_name_fields(self) -> str:
        """Return refugee fields used to build record_name."""
        return G2PRegisterDomainServiceRefugee().construct_record_name(self.to_dict())

    def get_search_text_fields(self) -> str:
        """Return refugee fields used to build search_text."""
        return G2PRegisterDomainServiceRefugee().construct_search_text(self.to_dict())
