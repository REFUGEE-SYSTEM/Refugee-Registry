import logging

from openg2p_registry_core.services import G2PRegisterDomainService

from .domain_validation_utils import (
    build_search_text,
    fallback_record_name,
    parse_date,
    validate_enum_values,
    validation_error,
)

_logger = logging.getLogger("g2p-register-domain-service")


def _enum_fields() -> dict:
    from ..models.enums import DocumentTypeEnum, IssuerTypeEnum

    return {
        "document_type": DocumentTypeEnum,
        "issuer_type": IssuerTypeEnum,
    }


class G2PRegisterDomainServiceIdentityDocument(G2PRegisterDomainService):
    async def validate_domain_attributes(self, records: list[dict]):
        for record in records:
            validate_enum_values(record, _enum_fields())
            issue_date = parse_date(record.get("issue_date"))
            expiry_date = parse_date(record.get("expiry_date"))
            if issue_date and expiry_date and expiry_date < issue_date:
                validation_error("expiry_date must be on or after issue_date")

    def construct_search_text(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing search text for identity document")
        keys = ["document_type", "document_number", "issuer_type"]
        return build_search_text(payload, keys, extra)

    def construct_record_name(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing record name for identity document")
        parts = []
        if extra:
            parts.extend(str(item).strip() for item in extra if str(item).strip())
        for key in ("document_type", "document_number"):
            val = str(payload.get(key) or "").strip()
            if val:
                parts.append(val)
        return " ".join(parts).strip() or fallback_record_name(
            payload, "IdentityDocument"
        )
