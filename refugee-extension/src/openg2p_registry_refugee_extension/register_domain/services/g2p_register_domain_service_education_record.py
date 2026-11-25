import logging
from datetime import date

from openg2p_registry_core.services import G2PRegisterDomainService

from .domain_validation_utils import (
    as_int,
    build_search_text,
    fallback_record_name,
    validate_enum_values,
    validation_error,
)

_logger = logging.getLogger("g2p-register-domain-service")


def _enum_fields() -> dict:
    from ..models.enums import HighestEducationLevelEnum

    return {"level": HighestEducationLevelEnum}


class G2PRegisterDomainServiceEducationRecord(G2PRegisterDomainService):
    async def validate_domain_attributes(self, records: list[dict]):
        current_year = date.today().year
        for record in records:
            validate_enum_values(record, _enum_fields())
            year = as_int(record.get("year_completed"))
            if year is not None and (year < 1900 or year > current_year):
                validation_error(
                    f"year_completed must be between 1900 and {current_year}"
                )

    def construct_search_text(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing search text for education record")
        keys = ["level", "institution", "field_of_study", "year_completed"]
        return build_search_text(payload, keys, extra)

    def construct_record_name(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing record name for education record")
        parts = []
        if extra:
            parts.extend(str(item).strip() for item in extra if str(item).strip())
        for key in ("level", "institution"):
            val = str(payload.get(key) or "").strip()
            if val:
                parts.append(val)
        return " ".join(parts).strip() or fallback_record_name(
            payload, "EducationRecord"
        )
