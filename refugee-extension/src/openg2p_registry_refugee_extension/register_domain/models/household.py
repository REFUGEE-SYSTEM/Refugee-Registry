from datetime import date, datetime

from openg2p_registry_core.models import (
    G2PGeo,
    G2PGeoHistory,
    G2PRegister,
    G2PRegisterHistory,
)
from openg2p_registry_core.models.g2p_intake_form import G2PIntakeForm
from sqlalchemy import Boolean, Date, DateTime, Float, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from ..services import G2PRegisterDomainServiceHousehold
from .enums import (
    DeliveryMechanismEnum,
    DeliveryModalityEnum,
    ExitReasonEnum,
    IncomeSourceEnum,
    LegalStatusEnum,
    PaymentStatusEnum,
    RefugeeRecordStatusEnum,
)


class G2PHousehold:
    """Domain attributes for Refugee Household (Uganda mandatory model + preserved legacy columns)."""

    # Legacy columns (preserved, never dropped)
    group_size: Mapped[int] = mapped_column(Integer, nullable=True)  # F03
    number_of_male: Mapped[int] = mapped_column(Integer, nullable=True)
    number_of_female: Mapped[int] = mapped_column(Integer, nullable=True)
    number_of_children: Mapped[int] = mapped_column(Integer, nullable=True)
    date_of_arrival: Mapped[date] = mapped_column(Date, nullable=True)
    registration_date: Mapped[date] = mapped_column(Date, nullable=True)  # A02
    legal_status: Mapped[LegalStatusEnum] = mapped_column(String, nullable=True)
    current_country_of_asylum_address: Mapped[str] = mapped_column(Text, nullable=True)
    country_of_origin: Mapped[str] = mapped_column(String, nullable=True)
    phone_number: Mapped[str] = mapped_column(String, nullable=True)
    consent_or_prohibition_to_share_information: Mapped[bool] = mapped_column(
        Boolean, nullable=True
    )

    # Uganda Mandatory Household attributes
    entry_point: Mapped[str] = mapped_column(String, nullable=True)  # A04
    registration_site: Mapped[str] = mapped_column(String, nullable=True)  # A05
    registering_officer_id: Mapped[str] = mapped_column(String, nullable=True)  # A06
    head_of_household_id: Mapped[str] = mapped_column(String, nullable=True)  # F01
    dependency_ratio: Mapped[float] = mapped_column(Float, nullable=True)  # F04
    is_female_headed: Mapped[bool] = mapped_column(Boolean, nullable=True)  # F05
    is_child_headed: Mapped[bool] = mapped_column(Boolean, nullable=True)  # F06
    host_district: Mapped[str] = mapped_column(String, nullable=True)  # G01
    settlement_location: Mapped[str] = mapped_column(String, nullable=True)  # G02
    zone_cluster: Mapped[str] = mapped_column(String, nullable=True)  # G03
    village_block: Mapped[str] = mapped_column(String, nullable=True)  # G04
    main_income_source: Mapped[IncomeSourceEnum] = mapped_column(String, nullable=True)  # L01
    working_age_earners: Mapped[int] = mapped_column(Integer, nullable=True)  # L02
    assistance_category: Mapped[str] = mapped_column(String, nullable=True)  # M01
    vulnerability_score: Mapped[int] = mapped_column(Integer, nullable=True)  # M02
    is_new_arrival: Mapped[bool] = mapped_column(Boolean, nullable=True)  # M03
    new_arrival_end_date: Mapped[date] = mapped_column(Date, nullable=True)  # M03
    programmes_enrolled: Mapped[list] = mapped_column(JSONB, nullable=True)  # M04
    enrolment_date: Mapped[date] = mapped_column(Date, nullable=True)  # M05
    exit_date: Mapped[date] = mapped_column(Date, nullable=True)  # M05
    exit_reason: Mapped[ExitReasonEnum] = mapped_column(String, nullable=True)  # M05
    delivery_modality: Mapped[DeliveryModalityEnum] = mapped_column(String, nullable=True)  # N01
    delivery_mechanism: Mapped[DeliveryMechanismEnum] = mapped_column(String, nullable=True)  # N01
    primary_recipient_id: Mapped[str] = mapped_column(String, nullable=True)  # N06
    food_distribution_point: Mapped[str] = mapped_column(String, nullable=True)  # N08
    entitlement_amount: Mapped[float] = mapped_column(Float, nullable=True)  # N09
    entitlement_currency: Mapped[str] = mapped_column(String, nullable=True)  # N09
    payment_cycle: Mapped[str] = mapped_column(String, nullable=True)  # O01
    payment_status: Mapped[PaymentStatusEnum] = mapped_column(String, nullable=True)  # O03
    transaction_reference: Mapped[str] = mapped_column(String, nullable=True)  # O04
    transaction_date: Mapped[date] = mapped_column(Date, nullable=True)  # O04
    lifecycle_status: Mapped[RefugeeRecordStatusEnum] = mapped_column(String, nullable=True)  # Q01
    last_updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)  # Q04
    last_updated_by: Mapped[str] = mapped_column(String, nullable=True)  # Q04


class G2PRegisterHousehold(G2PRegister, G2PGeo, G2PHousehold):
    __tablename__ = "g2p_register_households"

    def get_search_text_fields(self) -> str:
        """Return household fields used to build search_text."""
        return G2PRegisterDomainServiceHousehold().construct_search_text(self.to_dict())

    def get_record_name_fields(self) -> str:
        """Return household record_name from domain service implementation."""
        return G2PRegisterDomainServiceHousehold().construct_record_name(self.to_dict())


class G2PRegisterHistoryHousehold(G2PRegisterHistory, G2PGeoHistory, G2PHousehold):
    __tablename__ = "g2p_register_history_households"


class G2PIntakeFormHousehold(G2PIntakeForm, G2PRegister, G2PGeo, G2PHousehold):
    __tablename__ = "g2p_intake_form_households"

    def get_search_text_fields(self) -> str:
        """Return household fields used to build search_text."""
        return G2PRegisterDomainServiceHousehold().construct_search_text(self.to_dict())

    def get_record_name_fields(self) -> str:
        """Return household record_name from domain service implementation."""
        return G2PRegisterDomainServiceHousehold().construct_record_name(self.to_dict())
