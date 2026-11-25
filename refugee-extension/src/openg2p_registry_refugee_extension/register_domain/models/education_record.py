from openg2p_registry_core.models import G2PRegister, G2PRegisterHistory
from openg2p_registry_core.models.g2p_intake_form import G2PIntakeForm
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..services import G2PRegisterDomainServiceEducationRecord
from .enums import HighestEducationLevelEnum


class G2PEducationRecord:
    """Domain attributes for Refugee EducationRecord TABLE register."""

    level: Mapped[HighestEducationLevelEnum] = mapped_column(String, nullable=True)
    institution: Mapped[str] = mapped_column(String, nullable=True)  # PROVISIONAL
    field_of_study: Mapped[str] = mapped_column(String, nullable=True)  # PROVISIONAL
    year_completed: Mapped[int] = mapped_column(Integer, nullable=True)  # PROVISIONAL


class G2PRegisterEducationRecord(G2PRegister, G2PEducationRecord):
    __tablename__ = "g2p_register_education_records"

    def get_search_text_fields(self) -> str:
        return G2PRegisterDomainServiceEducationRecord().construct_search_text(
            self.to_dict()
        )

    def get_record_name_fields(self) -> str:
        return G2PRegisterDomainServiceEducationRecord().construct_record_name(
            self.to_dict()
        )


class G2PRegisterHistoryEducationRecord(G2PRegisterHistory, G2PEducationRecord):
    __tablename__ = "g2p_register_history_education_records"


class G2PIntakeFormEducationRecord(G2PIntakeForm, G2PRegister, G2PEducationRecord):
    __tablename__ = "g2p_intake_form_education_records"

    def get_search_text_fields(self) -> str:
        return G2PRegisterDomainServiceEducationRecord().construct_search_text(
            self.to_dict()
        )

    def get_record_name_fields(self) -> str:
        return G2PRegisterDomainServiceEducationRecord().construct_record_name(
            self.to_dict()
        )
