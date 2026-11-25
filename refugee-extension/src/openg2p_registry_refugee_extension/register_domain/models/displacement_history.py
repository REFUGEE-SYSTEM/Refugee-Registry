from datetime import date

from openg2p_registry_core.models import G2PRegister, G2PRegisterHistory
from openg2p_registry_core.models.g2p_intake_form import G2PIntakeForm
from sqlalchemy import Date, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..services import G2PRegisterDomainServiceDisplacementHistory


class G2PDisplacementHistory:
    """Domain attributes for Refugee DisplacementHistory TABLE register."""

    reasons_for_unwillingness_or_inability_to_return: Mapped[str] = mapped_column(
        Text, nullable=True
    )
    travel_details: Mapped[str] = mapped_column(Text, nullable=True)
    departure_date: Mapped[date] = mapped_column(Date, nullable=True)  # PROVISIONAL
    transit_countries: Mapped[str] = mapped_column(Text, nullable=True)  # PROVISIONAL


class G2PRegisterDisplacementHistory(G2PRegister, G2PDisplacementHistory):
    __tablename__ = "g2p_register_displacement_histories"

    def get_search_text_fields(self) -> str:
        return G2PRegisterDomainServiceDisplacementHistory().construct_search_text(
            self.to_dict()
        )

    def get_record_name_fields(self) -> str:
        return G2PRegisterDomainServiceDisplacementHistory().construct_record_name(
            self.to_dict()
        )


class G2PRegisterHistoryDisplacementHistory(
    G2PRegisterHistory, G2PDisplacementHistory
):
    __tablename__ = "g2p_register_history_displacement_histories"


class G2PIntakeFormDisplacementHistory(
    G2PIntakeForm, G2PRegister, G2PDisplacementHistory
):
    __tablename__ = "g2p_intake_form_displacement_histories"

    def get_search_text_fields(self) -> str:
        return G2PRegisterDomainServiceDisplacementHistory().construct_search_text(
            self.to_dict()
        )

    def get_record_name_fields(self) -> str:
        return G2PRegisterDomainServiceDisplacementHistory().construct_record_name(
            self.to_dict()
        )
