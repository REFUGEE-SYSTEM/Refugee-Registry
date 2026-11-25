import logging
from datetime import date

from openg2p_registry_core.services import G2PRegisterDomainService

from .domain_validation_utils import (
    build_search_text,
    fallback_record_name,
    parse_date,
    validation_error,
)

_logger = logging.getLogger("g2p-register-domain-service")


class G2PRegisterDomainServiceDisplacementHistory(G2PRegisterDomainService):
    async def validate_domain_attributes(self, records: list[dict]):
        today = date.today()
        for record in records:
            departure = parse_date(record.get("departure_date"))
            if departure is not None and departure > today:
                validation_error("departure_date must not be in the future")

    def construct_search_text(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing search text for displacement history")
        keys = [
            "reasons_for_unwillingness_or_inability_to_return",
            "travel_details",
            "transit_countries",
        ]
        return build_search_text(payload, keys, extra)

    def construct_record_name(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing record name for displacement history")
        parts = []
        if extra:
            parts.extend(str(item).strip() for item in extra if str(item).strip())
        for key in ("departure_date", "transit_countries"):
            val = str(payload.get(key) or "").strip()
            if val:
                parts.append(val)
        return " ".join(parts).strip() or fallback_record_name(
            payload, "DisplacementHistory"
        )
