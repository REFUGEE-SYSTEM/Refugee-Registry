from datetime import date

from openg2p_registry_core.models import G2PRegister, G2PRegisterHistory
from openg2p_registry_core.models.g2p_intake_form import G2PIntakeForm
from sqlalchemy import Date, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..services import G2PRegisterDomainServiceSpecificNeeds
from .enums import NeedCategoryEnum, NeedSeverityEnum


class G2PSpecificNeeds:
    """Domain attributes for Refugee SpecificNeeds TABLE register (PROVISIONAL)."""

    need_category: Mapped[NeedCategoryEnum] = mapped_column(String, nullable=True)  # PROVISIONAL
    severity: Mapped[NeedSeverityEnum] = mapped_column(String, nullable=True)  # PROVISIONAL
    date_identified: Mapped[date] = mapped_column(Date, nullable=True)  # PROVISIONAL
    support_required: Mapped[str] = mapped_column(Text, nullable=True)  # PROVISIONAL
    notes: Mapped[str] = mapped_column(Text, nullable=True)  # PROVISIONAL


class G2PRegisterSpecificNeeds(G2PRegister, G2PSpecificNeeds):
    __tablename__ = "g2p_register_specific_needs"

    def get_search_text_fields(self) -> str:
        return G2PRegisterDomainServiceSpecificNeeds().construct_search_text(
            self.to_dict()
        )

    def get_record_name_fields(self) -> str:
        return G2PRegisterDomainServiceSpecificNeeds().construct_record_name(
            self.to_dict()
        )


class G2PRegisterHistorySpecificNeeds(G2PRegisterHistory, G2PSpecificNeeds):
    __tablename__ = "g2p_register_history_specific_needs"


class G2PIntakeFormSpecificNeeds(G2PIntakeForm, G2PRegister, G2PSpecificNeeds):
    __tablename__ = "g2p_intake_form_specific_needs"

    def get_search_text_fields(self) -> str:
        return G2PRegisterDomainServiceSpecificNeeds().construct_search_text(
            self.to_dict()
        )

    def get_record_name_fields(self) -> str:
        return G2PRegisterDomainServiceSpecificNeeds().construct_record_name(
            self.to_dict()
        )
