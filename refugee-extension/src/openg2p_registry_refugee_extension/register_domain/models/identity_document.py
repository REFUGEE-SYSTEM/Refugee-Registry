from datetime import date

from openg2p_registry_core.models import G2PRegister, G2PRegisterHistory
from openg2p_registry_core.models.g2p_intake_form import G2PIntakeForm
from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column

from ..services import G2PRegisterDomainServiceIdentityDocument
from .enums import DocumentTypeEnum, IssuerTypeEnum


class G2PIdentityDocument:
    """Domain attributes for Refugee IdentityDocument TABLE register."""

    document_type: Mapped[DocumentTypeEnum] = mapped_column(String, nullable=True)
    document_number: Mapped[str] = mapped_column(String, nullable=True)
    issuer_type: Mapped[IssuerTypeEnum] = mapped_column(String, nullable=True)  # PROVISIONAL
    issue_date: Mapped[date] = mapped_column(Date, nullable=True)  # PROVISIONAL
    expiry_date: Mapped[date] = mapped_column(Date, nullable=True)  # PROVISIONAL


class G2PRegisterIdentityDocument(G2PRegister, G2PIdentityDocument):
    __tablename__ = "g2p_register_identity_documents"

    def get_search_text_fields(self) -> str:
        return G2PRegisterDomainServiceIdentityDocument().construct_search_text(
            self.to_dict()
        )

    def get_record_name_fields(self) -> str:
        return G2PRegisterDomainServiceIdentityDocument().construct_record_name(
            self.to_dict()
        )


class G2PRegisterHistoryIdentityDocument(G2PRegisterHistory, G2PIdentityDocument):
    __tablename__ = "g2p_register_history_identity_documents"


class G2PIntakeFormIdentityDocument(
    G2PIntakeForm, G2PRegister, G2PIdentityDocument
):
    __tablename__ = "g2p_intake_form_identity_documents"

    def get_search_text_fields(self) -> str:
        return G2PRegisterDomainServiceIdentityDocument().construct_search_text(
            self.to_dict()
        )

    def get_record_name_fields(self) -> str:
        return G2PRegisterDomainServiceIdentityDocument().construct_record_name(
            self.to_dict()
        )
