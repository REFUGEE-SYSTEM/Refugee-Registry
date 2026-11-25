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
    from ..models.enums import NeedCategoryEnum, NeedSeverityEnum

    return {
        "need_category": NeedCategoryEnum,
        "severity": NeedSeverityEnum,
    }


class G2PRegisterDomainServiceSpecificNeeds(G2PRegisterDomainService):
    async def validate_domain_attributes(self, records: list[dict]):
        today = date.today()
        for record in records:
            validate_enum_values(record, _enum_fields())
            date_identified = parse_date(record.get("date_identified"))
            if date_identified is not None and date_identified > today:
                validation_error("date_identified must not be in the future")

    def construct_search_text(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing search text for specific needs")
        keys = ["need_category", "severity", "support_required", "notes"]
        return build_search_text(payload, keys, extra)

    def construct_record_name(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing record name for specific needs")
        parts = []
        if extra:
            parts.extend(str(item).strip() for item in extra if str(item).strip())
        for key in ("need_category", "severity"):
            val = str(payload.get(key) or "").strip()
            if val:
                parts.append(val)
        return " ".join(parts).strip() or fallback_record_name(
            payload, "SpecificNeeds"
        )
