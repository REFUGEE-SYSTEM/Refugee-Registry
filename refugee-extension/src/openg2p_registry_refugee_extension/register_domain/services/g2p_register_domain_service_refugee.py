import logging
from datetime import date, datetime, timezone

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
    from ..models.enums import (
        AuthResultEnum,
        DuplicateCheckEnum,
        ExitReasonEnum,
        HighestEducationLevelEnum,
        LegalStatusEnum,
        PresenceStatusEnum,
        RefugeeGenderEnum,
        RefugeeMaritalStatusEnum,
        RefugeeRecordStatusEnum,
        ReligionEnum,
        SecurityScreeningEnum,
        UnaccompaniedChildEnum,
        WashingtonGroupAnswerEnum,
    )

    return {
        "gender": RefugeeGenderEnum,
        "marital_status": RefugeeMaritalStatusEnum,
        "highest_education_level": HighestEducationLevelEnum,
        "religion": ReligionEnum,
        "legal_status": LegalStatusEnum,
        "security_screening_status": SecurityScreeningEnum,
        "presence_status": PresenceStatusEnum,
        "unaccompanied_separated_status": UnaccompaniedChildEnum,
        "wg_seeing": WashingtonGroupAnswerEnum,
        "wg_hearing": WashingtonGroupAnswerEnum,
        "wg_walking": WashingtonGroupAnswerEnum,
        "wg_remembering": WashingtonGroupAnswerEnum,
        "wg_self_care": WashingtonGroupAnswerEnum,
        "wg_communicating": WashingtonGroupAnswerEnum,
        "exit_reason": ExitReasonEnum,
        "auth_result": AuthResultEnum,
        "lifecycle_status": RefugeeRecordStatusEnum,
        "duplicate_check_result": DuplicateCheckEnum,
    }


class G2PRegisterDomainServiceRefugee(G2PRegisterDomainService):
    async def validate_domain_attributes(self, records: list[dict]):
        for record in records:
            validate_enum_values(record, _enum_fields())
            self._validate_dates(record)
            self._validate_list_fields(record)
            self._normalize_and_audit(record)

    def _validate_dates(self, record: dict) -> None:
        today = date.today()
        for field in (
            "birth_date",
            "arrival_date",
            "rsd_application_date",
            "enrolment_date",
            "informed_consent_date",
        ):
            d = parse_date(record.get(field))
            if d is not None and d > today:
                validation_error(f"{field} must not be in the future")

    def _validate_list_fields(self, record: dict) -> None:
        for field in ("languages_known", "programmes_enrolled", "partner_data_sharing_consent"):
            vals = record.get(field)
            if vals is None:
                continue
            if not isinstance(vals, list):
                validation_error(f"{field} must be a list of codes")
            cleaned = [str(item).strip() for item in vals if item is not None and str(item).strip()]
            if len(cleaned) != len(vals):
                validation_error(f"{field} must not contain empty values")

    def _normalize_and_audit(self, record: dict) -> None:
        if record.get("last_name"):
            record["last_name"] = str(record["last_name"]).strip().upper()
        if not record.get("last_updated_at"):
            record["last_updated_at"] = datetime.now(timezone.utc).replace(tzinfo=None)

    def construct_search_text(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing search text for refugee")
        keys = [
            "functional_record_id",
            "foundational_id",
            "first_name",
            "middle_name",
            "last_name",
            "given_name",
            "gender",
            "birth_date",
            "place_of_birth",
            "country_of_origin",
            "nationality",
            "marital_status",
            "legal_status",
            "security_screening_status",
            "presence_status",
            "languages_known",
            "lifecycle_status",
        ]
        return build_search_text(payload, keys, extra)

    def construct_record_name(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing record name for refugee")
        parts = []
        if extra:
            parts.extend(str(item).strip() for item in extra if str(item).strip())
        for key in ("given_name", "first_name", "middle_name", "last_name"):
            val = str(payload.get(key) or "").strip()
            if val and val not in parts:
                parts.append(val)
        return " ".join(parts).strip() or fallback_record_name(payload, "Refugee")

    def construct_intake_record_name(
        self, payload: dict, extra: list[str] = None
    ) -> str:
        name = self.construct_record_name(payload, extra)
        app_ref = str(payload.get("application_reference") or "").strip()
        if app_ref and app_ref not in name:
            return f"{name} ({app_ref})".strip()
        return name
