import logging
from datetime import date

from openg2p_registry_core.services import G2PRegisterDomainService

from .domain_validation_utils import (
    as_int,
    build_search_text,
    fallback_record_name,
    is_blank,
    parse_date,
    validate_enum_values,
    validation_error,
)

_logger = logging.getLogger("g2p-register-domain-service")


def _enum_fields() -> dict:
    from ..models.enums import LegalStatusEnum

    return {"legal_status": LegalStatusEnum}


class G2PRegisterDomainServiceHousehold(G2PRegisterDomainService):
    async def validate_domain_attributes(self, records: list[dict]):
        for record in records:
            validate_enum_values(record, _enum_fields())
            self._validate_group_counts(record)
            self._validate_dates(record)

    def _validate_group_counts(self, record: dict) -> None:
        group_size = as_int(record.get("group_size"))
        male = as_int(record.get("number_of_male"))
        female = as_int(record.get("number_of_female"))
        children = as_int(record.get("number_of_children"))

        for label, value in (
            ("group_size", group_size),
            ("number_of_male", male),
            ("number_of_female", female),
            ("number_of_children", children),
        ):
            if value is not None and value < 0:
                validation_error(f"{label} must not be negative")

        if group_size is not None and group_size < 1:
            validation_error("group_size must be at least 1")

        if (
            group_size is not None
            and male is not None
            and female is not None
            and male + female > group_size
        ):
            validation_error(
                "number_of_male + number_of_female must not exceed group_size"
            )

        if group_size is not None and children is not None and children > group_size:
            validation_error("number_of_children must not exceed group_size")

    def _validate_dates(self, record: dict) -> None:
        today = date.today()
        arrival = parse_date(record.get("date_of_arrival"))
        reg_date = parse_date(record.get("registration_date"))
        if arrival is not None and arrival > today:
            validation_error("date_of_arrival must not be in the future")
        if reg_date is not None and reg_date > today:
            validation_error("registration_date must not be in the future")

    def construct_search_text(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing search text for household")
        keys = [
            "functional_record_id",
            "record_name",
            "legal_status",
            "country_of_origin",
            "current_country_of_asylum_address",
            "phone_number",
            "latitude",
            "longitude",
            "plus_code",
            "address_line_1",
            "address_line_2",
            "postal_code",
            "country_code",
        ]
        return build_search_text(payload, keys, extra)

    def construct_record_name(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing record name for household")
        parts = []
        if extra:
            parts.extend(str(item).strip() for item in extra if str(item).strip())
        for key in ("functional_record_id", "country_of_origin", "legal_status"):
            val = str(payload.get(key) or "").strip()
            if val:
                parts.append(val)
        return " ".join(parts).strip() or fallback_record_name(payload, "Household")

    def construct_intake_record_name(
        self, payload: dict, extra: list[str] = None
    ) -> str:
        name = self.construct_record_name(payload, extra)
        app_ref = str(payload.get("application_reference") or "").strip()
        if app_ref and app_ref not in name:
            return f"{name} ({app_ref})".strip()
        return name
