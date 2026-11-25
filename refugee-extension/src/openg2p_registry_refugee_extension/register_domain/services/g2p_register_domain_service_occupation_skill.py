import logging

from openg2p_registry_core.services import G2PRegisterDomainService

from .domain_validation_utils import (
    as_int,
    build_search_text,
    fallback_record_name,
    validation_error,
)

_logger = logging.getLogger("g2p-register-domain-service")


class G2PRegisterDomainServiceOccupationSkill(G2PRegisterDomainService):
    async def validate_domain_attributes(self, records: list[dict]):
        for record in records:
            years = as_int(record.get("years_of_experience"))
            if years is not None and years < 0:
                validation_error("years_of_experience must not be negative")

    def construct_search_text(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing search text for occupation skill")
        keys = ["occupation", "skill", "years_of_experience"]
        return build_search_text(payload, keys, extra)

    def construct_record_name(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing record name for occupation skill")
        parts = []
        if extra:
            parts.extend(str(item).strip() for item in extra if str(item).strip())
        for key in ("occupation", "skill"):
            val = str(payload.get(key) or "").strip()
            if val:
                parts.append(val)
        return " ".join(parts).strip() or fallback_record_name(
            payload, "OccupationSkill"
        )
