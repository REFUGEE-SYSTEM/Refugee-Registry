from datetime import date

from openg2p_registry_core.models import G2PRegister, G2PRegisterHistory
from openg2p_registry_core.models.g2p_intake_form import G2PIntakeForm
from sqlalchemy import Date, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..services import G2PRegisterDomainServiceRelative
from .enums import RelativeRelationshipEnum


class G2PRelative:
    """Domain attributes for Refugee Relative TABLE register (PROVISIONAL)."""

    relationship: Mapped[RelativeRelationshipEnum] = mapped_column(
        String, nullable=True
    )  # PROVISIONAL
    full_name: Mapped[str] = mapped_column(String, nullable=True)  # PROVISIONAL
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=True)  # PROVISIONAL
    location_or_status: Mapped[str] = mapped_column(Text, nullable=True)  # PROVISIONAL


class G2PRegisterRelative(G2PRegister, G2PRelative):
    __tablename__ = "g2p_register_relatives"

    def get_search_text_fields(self) -> str:
        return G2PRegisterDomainServiceRelative().construct_search_text(self.to_dict())

    def get_record_name_fields(self) -> str:
        return G2PRegisterDomainServiceRelative().construct_record_name(self.to_dict())


class G2PRegisterHistoryRelative(G2PRegisterHistory, G2PRelative):
    __tablename__ = "g2p_register_history_relatives"


class G2PIntakeFormRelative(G2PIntakeForm, G2PRegister, G2PRelative):
    __tablename__ = "g2p_intake_form_relatives"

    def get_search_text_fields(self) -> str:
        return G2PRegisterDomainServiceRelative().construct_search_text(self.to_dict())

    def get_record_name_fields(self) -> str:
        return G2PRegisterDomainServiceRelative().construct_record_name(self.to_dict())
