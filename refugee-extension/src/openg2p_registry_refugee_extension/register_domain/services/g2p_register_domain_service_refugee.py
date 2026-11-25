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
    from ..models.enums import (
        HighestEducationLevelEnum,
        RelationshipToGroupEnum,
        ReligionEnum,
    )

    return {
        "relationship_to_group": RelationshipToGroupEnum,
        "highest_education_level": HighestEducationLevelEnum,
        "religion": ReligionEnum,
    }


class G2PRegisterDomainServiceRefugee(G2PRegisterDomainService):
    async def validate_domain_attributes(self, records: list[dict]):
        for record in records:
            validate_enum_values(record, _enum_fields())
            self._validate_birth_date(record)
            self._validate_languages_known(record)

    def _validate_birth_date(self, record: dict) -> None:
        birth_date = parse_date(record.get("birth_date"))
        if birth_date is not None and birth_date > date.today():
            validation_error("birth_date must not be in the future")

    def _validate_languages_known(self, record: dict) -> None:
        langs = record.get("languages_known")
        if langs is None:
            return
        if not isinstance(langs, list):
            validation_error("languages_known must be a list of language codes")
        cleaned = [str(item).strip() for item in langs if item is not None and str(item).strip()]
        if len(cleaned) != len(langs):
            validation_error("languages_known must not contain empty values")

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
            "marital_status",
            "relationship_to_group",
            "country_of_origin",
            "fathers_name",
            "mothers_name",
            "highest_education_level",
            "last_occupation",
            "religion",
            "languages_known",
            "place_of_birth",
        ]
        return build_search_text(payload, keys, extra)

    def construct_record_name(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing record name for refugee")
        parts = []
        if extra:
            parts.extend(str(item).strip() for item in extra if str(item).strip())
        for key in ("first_name", "middle_name", "last_name"):
            val = str(payload.get(key) or "").strip()
            if val:
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
