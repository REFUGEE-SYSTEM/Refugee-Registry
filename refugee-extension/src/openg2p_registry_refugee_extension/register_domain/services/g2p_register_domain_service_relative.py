import logging
from datetime import date

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
    from ..models.enums import RelativeRelationshipEnum

    return {"relationship": RelativeRelationshipEnum}


class G2PRegisterDomainServiceRelative(G2PRegisterDomainService):
    async def validate_domain_attributes(self, records: list[dict]):
        today = date.today()
        for record in records:
            validate_enum_values(record, _enum_fields())
            dob = parse_date(record.get("date_of_birth"))
            if dob is not None and dob > today:
                validation_error("date_of_birth must not be in the future")

    def construct_search_text(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing search text for relative")
        keys = ["relationship", "full_name", "location_or_status"]
        return build_search_text(payload, keys, extra)

    def construct_record_name(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing record name for relative")
        parts = []
        if extra:
            parts.extend(str(item).strip() for item in extra if str(item).strip())
        for key in ("full_name", "relationship"):
            val = str(payload.get(key) or "").strip()
            if val:
                parts.append(val)
        return " ".join(parts).strip() or fallback_record_name(payload, "Relative")
