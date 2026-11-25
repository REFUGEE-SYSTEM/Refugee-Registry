import logging
from datetime import date, datetime, timezone

from openg2p_registry_core.services import G2PRegisterDomainService

from .domain_validation_utils import (
    as_int,
    build_search_text,
    fallback_record_name,
    parse_date,
    validate_enum_values,
    validation_error,
)

_logger = logging.getLogger("g2p-register-domain-service")


def _enum_fields() -> dict:
    from ..models.enums import (
        DeliveryMechanismEnum,
        DeliveryModalityEnum,
        ExitReasonEnum,
        IncomeSourceEnum,
        LegalStatusEnum,
        PaymentStatusEnum,
        RefugeeRecordStatusEnum,
    )

    return {
        "legal_status": LegalStatusEnum,
        "main_income_source": IncomeSourceEnum,
        "exit_reason": ExitReasonEnum,
        "delivery_modality": DeliveryModalityEnum,
        "delivery_mechanism": DeliveryMechanismEnum,
        "payment_status": PaymentStatusEnum,
        "lifecycle_status": RefugeeRecordStatusEnum,
    }


class G2PRegisterDomainServiceHousehold(G2PRegisterDomainService):
    async def validate_domain_attributes(self, records: list[dict]):
        for record in records:
            validate_enum_values(record, _enum_fields())
            self._validate_group_counts(record)
            self._validate_uganda_fields(record)
            self._validate_dates(record)
            self._populate_derived_and_audit(record)

    def _validate_group_counts(self, record: dict) -> None:
        group_size = as_int(record.get("group_size"))
        male = as_int(record.get("number_of_male"))
        female = as_int(record.get("number_of_female"))
        children = as_int(record.get("number_of_children"))
        earners = as_int(record.get("working_age_earners"))

        for label, value in (
            ("group_size", group_size),
            ("number_of_male", male),
            ("number_of_female", female),
            ("number_of_children", children),
            ("working_age_earners", earners),
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

    def _validate_uganda_fields(self, record: dict) -> None:
        vuln = as_int(record.get("vulnerability_score"))
        if vuln is not None and not (0 <= vuln <= 100):
            validation_error("vulnerability_score must be between 0 and 100")

        dep_ratio = record.get("dependency_ratio")
        if dep_ratio is not None and dep_ratio != "":
            try:
                if float(dep_ratio) < 0:
                    validation_error("dependency_ratio must not be negative")
            except (TypeError, ValueError):
                validation_error("dependency_ratio must be a number")

        ent_amt = record.get("entitlement_amount")
        if ent_amt is not None and ent_amt != "":
            try:
                if float(ent_amt) < 0:
                    validation_error("entitlement_amount must not be negative")
            except (TypeError, ValueError):
                validation_error("entitlement_amount must be a number")

    def _validate_dates(self, record: dict) -> None:
        today = date.today()
        for field in ("date_of_arrival", "registration_date", "enrolment_date", "transaction_date"):
            d = parse_date(record.get(field))
            if d is not None and d > today:
                validation_error(f"{field} must not be in the future")

    def _populate_derived_and_audit(self, record: dict) -> None:
        if not record.get("entitlement_currency"):
            record["entitlement_currency"] = "UGX"
        if not record.get("last_updated_at"):
            record["last_updated_at"] = datetime.now(timezone.utc).replace(tzinfo=None)

    def construct_search_text(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing search text for household")
        keys = [
            "functional_record_id",
            "record_name",
            "host_district",
            "settlement_location",
            "zone_cluster",
            "village_block",
            "entry_point",
            "registration_site",
            "assistance_category",
            "delivery_modality",
            "payment_cycle",
            "payment_status",
            "transaction_reference",
            "lifecycle_status",
        ]
        return build_search_text(payload, keys, extra)

    def construct_record_name(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing record name for household")
        parts = []
        if extra:
            parts.extend(str(item).strip() for item in extra if str(item).strip())
        for key in ("functional_record_id", "settlement_location", "host_district"):
            val = str(payload.get(key) or "").strip()
            if val:
                parts.append(val)
        return " ".join(parts).strip() or fallback_record_name(payload, "Household")
