from openg2p_registry_core.models import G2PRegister, G2PRegisterHistory
from openg2p_registry_core.models.g2p_intake_form import G2PIntakeForm
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ..services import G2PRegisterDomainServiceAddress
from .enums import AddressTypeEnum


class G2PAddress:
    """Domain attributes for Refugee Address TABLE register (PROVISIONAL)."""

    address_type: Mapped[AddressTypeEnum] = mapped_column(
        String, nullable=True
    )  # PROVISIONAL
    address_line_1: Mapped[str] = mapped_column(String, nullable=True)  # PROVISIONAL
    address_line_2: Mapped[str] = mapped_column(String, nullable=True)  # PROVISIONAL
    country: Mapped[str] = mapped_column(String, nullable=True)  # PROVISIONAL


class G2PRegisterAddress(G2PRegister, G2PAddress):
    __tablename__ = "g2p_register_addresses"

    def get_search_text_fields(self) -> str:
        return G2PRegisterDomainServiceAddress().construct_search_text(self.to_dict())

    def get_record_name_fields(self) -> str:
        return G2PRegisterDomainServiceAddress().construct_record_name(self.to_dict())


class G2PRegisterHistoryAddress(G2PRegisterHistory, G2PAddress):
    __tablename__ = "g2p_register_history_addresses"


class G2PIntakeFormAddress(G2PIntakeForm, G2PRegister, G2PAddress):
    __tablename__ = "g2p_intake_form_addresses"

    def get_search_text_fields(self) -> str:
        return G2PRegisterDomainServiceAddress().construct_search_text(self.to_dict())

    def get_record_name_fields(self) -> str:
        return G2PRegisterDomainServiceAddress().construct_record_name(self.to_dict())
