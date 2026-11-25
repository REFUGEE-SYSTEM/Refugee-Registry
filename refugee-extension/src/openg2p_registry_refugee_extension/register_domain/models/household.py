from datetime import date

from openg2p_registry_core.models import (
    G2PGeo,
    G2PGeoHistory,
    G2PRegister,
    G2PRegisterHistory,
)
from openg2p_registry_core.models.g2p_intake_form import G2PIntakeForm
from sqlalchemy import Boolean, Date, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..services import G2PRegisterDomainServiceHousehold
from .enums import LegalStatusEnum


class G2PHousehold:
    """Domain attributes for Refugee Household (proGres case/group)."""

    group_size: Mapped[int] = mapped_column(Integer, nullable=True)
    number_of_male: Mapped[int] = mapped_column(Integer, nullable=True)
    number_of_female: Mapped[int] = mapped_column(Integer, nullable=True)
    number_of_children: Mapped[int] = mapped_column(Integer, nullable=True)
    date_of_arrival: Mapped[date] = mapped_column(Date, nullable=True)
    registration_date: Mapped[date] = mapped_column(Date, nullable=True)
    legal_status: Mapped[LegalStatusEnum] = mapped_column(String, nullable=True)
    current_country_of_asylum_address: Mapped[str] = mapped_column(Text, nullable=True)
    country_of_origin: Mapped[str] = mapped_column(String, nullable=True)
    phone_number: Mapped[str] = mapped_column(String, nullable=True)
    # Flagged: platform Consent Manager / data_scopes normally govern external
    # sharing; kept as a boolean column per proGres household intake requirements.
    consent_or_prohibition_to_share_information: Mapped[bool] = mapped_column(
        Boolean, nullable=True
    )


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
