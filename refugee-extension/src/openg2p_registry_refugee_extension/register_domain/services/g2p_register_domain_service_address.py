import logging

from openg2p_registry_core.services import G2PRegisterDomainService

from .domain_validation_utils import (
    build_search_text,
    fallback_record_name,
    validate_enum_values,
)

_logger = logging.getLogger("g2p-register-domain-service")


def _enum_fields() -> dict:
    from ..models.enums import AddressTypeEnum

    return {"address_type": AddressTypeEnum}


class G2PRegisterDomainServiceAddress(G2PRegisterDomainService):
    async def validate_domain_attributes(self, records: list[dict]):
        for record in records:
            validate_enum_values(record, _enum_fields())

    def construct_search_text(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing search text for address")
        keys = ["address_type", "address_line_1", "address_line_2", "country"]
        return build_search_text(payload, keys, extra)

    def construct_record_name(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing record name for address")
        parts = []
        if extra:
            parts.extend(str(item).strip() for item in extra if str(item).strip())
        for key in ("address_type", "address_line_1", "country"):
            val = str(payload.get(key) or "").strip()
            if val:
                parts.append(val)
        return " ".join(parts).strip() or fallback_record_name(payload, "Address")
