from datetime import date
from typing import Optional

from openg2p_registry_core.schemas import (
    G2PIntakeFormSchemaBase,
    G2PRegisterBaseSchema,
    G2PRegisterHistorySchema,
)

from ..models.enums import DocumentTypeEnum, IssuerTypeEnum


class G2PSchemaIdentityDocument:
    document_type: Optional[DocumentTypeEnum] = None
    document_number: Optional[str] = None
    issuer_type: Optional[IssuerTypeEnum] = None
    issue_date: Optional[date] = None
    expiry_date: Optional[date] = None


class G2PRegisterSchemaIdentityDocument(
    G2PRegisterBaseSchema, G2PSchemaIdentityDocument
):
    """Schema for IdentityDocument register."""


class G2PRegisterHistorySchemaIdentityDocument(
    G2PRegisterHistorySchema, G2PSchemaIdentityDocument
):
    """Schema for IdentityDocument history."""


class G2PIntakeFormSchemaIdentityDocument(
    G2PIntakeFormSchemaBase, G2PRegisterBaseSchema, G2PSchemaIdentityDocument
):
    """Schema for IdentityDocument intake form."""
