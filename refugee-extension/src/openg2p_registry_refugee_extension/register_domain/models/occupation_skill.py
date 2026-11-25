from openg2p_registry_core.models import G2PRegister, G2PRegisterHistory
from openg2p_registry_core.models.g2p_intake_form import G2PIntakeForm
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..services import G2PRegisterDomainServiceOccupationSkill


class G2POccupationSkill:
    """Domain attributes for Refugee OccupationSkill TABLE register (PROVISIONAL)."""

    occupation: Mapped[str] = mapped_column(String, nullable=True)  # PROVISIONAL
    skill: Mapped[str] = mapped_column(String, nullable=True)  # PROVISIONAL
    years_of_experience: Mapped[int] = mapped_column(
        Integer, nullable=True
    )  # PROVISIONAL


class G2PRegisterOccupationSkill(G2PRegister, G2POccupationSkill):
    __tablename__ = "g2p_register_occupation_skills"

    def get_search_text_fields(self) -> str:
        return G2PRegisterDomainServiceOccupationSkill().construct_search_text(
            self.to_dict()
        )

    def get_record_name_fields(self) -> str:
        return G2PRegisterDomainServiceOccupationSkill().construct_record_name(
            self.to_dict()
        )


class G2PRegisterHistoryOccupationSkill(G2PRegisterHistory, G2POccupationSkill):
    __tablename__ = "g2p_register_history_occupation_skills"


class G2PIntakeFormOccupationSkill(G2PIntakeForm, G2PRegister, G2POccupationSkill):
    __tablename__ = "g2p_intake_form_occupation_skills"

    def get_search_text_fields(self) -> str:
        return G2PRegisterDomainServiceOccupationSkill().construct_search_text(
            self.to_dict()
        )

    def get_record_name_fields(self) -> str:
        return G2PRegisterDomainServiceOccupationSkill().construct_record_name(
            self.to_dict()
        )
