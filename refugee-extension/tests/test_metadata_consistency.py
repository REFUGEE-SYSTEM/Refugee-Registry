import glob
import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock

if importlib.util.find_spec("openg2p_fastapi_common.crypto") is None:
    sys.modules["openg2p_fastapi_common.crypto"] = MagicMock()

from openg2p_registry_refugee_extension.register_domain import models, schemas, services
from openg2p_registry_refugee_extension.register_domain.constants import REGISTER_IDS
from openg2p_registry_refugee_extension.register_domain.id_generator.g2p_id_generator_service import (
    G2PIdGeneratorService,
)
from openg2p_registry_refugee_extension.register_domain.models.enums import (
    AddressTypeEnum,
    AuthResultEnum,
    DeliveryMechanismEnum,
    DeliveryModalityEnum,
    DocumentTypeEnum,
    DuplicateCheckEnum,
    ExitReasonEnum,
    HighestEducationLevelEnum,
    IncomeSourceEnum,
    IssuerTypeEnum,
    LegalStatusEnum,
    NeedCategoryEnum,
    NeedSeverityEnum,
    PaymentStatusEnum,
    PresenceStatusEnum,
    RefugeeGenderEnum,
    RefugeeMaritalStatusEnum,
    RefugeeRecordStatusEnum,
    RelationshipToGroupEnum,
    RelativeRelationshipEnum,
    ReligionEnum,
    SecurityScreeningEnum,
    UnaccompaniedChildEnum,
    WashingtonGroupAnswerEnum,
)

EXT_ROOT = Path(__file__).resolve().parents[1]
PKG_ROOT = EXT_ROOT / "src" / "openg2p_registry_refugee_extension"
META_DIR = PKG_ROOT / "meta_data" / "register-metadata"
WORKSPACE_ROOT = EXT_ROOT.parents[1]
PACK_ETH = WORKSPACE_ROOT / "openg2p-data" / "packs" / "ETH"


def _load_codelists() -> dict[str, dict]:
    codelists: dict[str, dict] = {}
    for folder in (PACK_ETH / "codelists", PACK_ETH / "domains" / "refugee"):
        for path in sorted(glob.glob(str(folder / "*.json"))):
            data = json.loads(Path(path).read_text(encoding="utf-8"))
            codelists[data["attribute_id"]] = data
    return codelists


def _codes(data: dict) -> set[str]:
    return {entry["value_code"] for entry in data.get("values", [])}


def _parse_section_schemas() -> list[tuple[str, str, dict]]:
    sql = (META_DIR / "g2p_register_sections.sql").read_text(encoding="utf-8")
    pattern = re.compile(
        r"\('([a-f0-9-]+)','([^']+)','([a-f0-9-]+)',[^,]+,[^,]+,[^,]+,[^,]+,\d+,[^,]+,\d+,'(\{.*?\})'",
        re.DOTALL,
    )
    rows = []
    for _reg_id, section_id, section_reg_id, raw_json in pattern.findall(sql):
        rows.append((section_id, section_reg_id, json.loads(raw_json.replace("''", "'"))))
    return rows


def _iter_widgets(obj):
    if isinstance(obj, dict):
        if "widget" in obj:
            yield obj
            if obj.get("widget") == "table":
                return
        for val in obj.values():
            yield from _iter_widgets(val)
    elif isinstance(obj, list):
        for item in obj:
            yield from _iter_widgets(item)


class MetadataConsistencyTests(unittest.TestCase):
    def test_every_register_has_models_schemas_and_service(self):
        for name, reg_id in REGISTER_IDS.items():
            self.assertTrue(hasattr(models, f"G2PRegister{name}"), f"Missing model G2PRegister{name}")
            self.assertTrue(hasattr(models, f"G2PRegisterHistory{name}"))
            self.assertTrue(hasattr(models, f"G2PIntakeForm{name}"))
            self.assertTrue(hasattr(schemas, f"G2PRegisterSchema{name}"))
            self.assertTrue(hasattr(services, f"G2PRegisterDomainService{name}"))
            self.assertTrue(reg_id.startswith("a0000000-"))

    def test_every_widget_path_resolves_to_orm_column(self):
        reg_to_orm = {
            reg_id: getattr(models, f"G2PRegister{name}")
            for name, reg_id in REGISTER_IDS.items()
        }
        sections = _parse_section_schemas()
        self.assertGreaterEqual(len(sections), 10)
        for section_id, section_reg_id, ui_schema in sections:
            orm_cls = reg_to_orm[section_reg_id]
            columns = {c.name for c in orm_cls.__table__.columns}
            for widget in _iter_widgets(ui_schema):
                if widget.get("widget") == "table":
                    for col in widget.get("widget-data-columns", []):
                        col_path = col.get("widget-data-path")
                        if isinstance(col_path, str):
                            self.assertIn(
                                col_path,
                                columns,
                                f"{section_id}: table column '{col_path}' not on {orm_cls.__name__}",
                            )
                    continue
                path_val = widget.get("widget-data-path")
                paths = (
                    list(path_val.values())
                    if isinstance(path_val, dict)
                    else ([path_val] if isinstance(path_val, str) else [])
                )
                for p in paths:
                    self.assertIn(".", p, f"{section_id}: widget-data-path '{p}' missing register prefix")
                    reg_prefix, field = p.split(".", 1)
                    self.assertEqual(reg_prefix, section_reg_id)
                    self.assertIn(
                        field,
                        columns,
                        f"{section_id}: field '{field}' not on {orm_cls.__name__}",
                    )

    def test_every_attribute_id_exists_in_core_or_refugee_domain(self):
        codelists = _load_codelists()
        sections = _parse_section_schemas()
        for section_id, _reg_id, ui_schema in sections:
            for widget in _iter_widgets(ui_schema):
                if widget.get("widget") == "table":
                    for col in widget.get("widget-data-columns", []):
                        ds = col.get("widget-data-source") or {}
                        attr_id = (ds.get("params") or {}).get("attribute_id")
                        if attr_id:
                            self.assertIn(
                                attr_id,
                                codelists,
                                f"{section_id}: attribute_id '{attr_id}' missing from ETH core/refugee packs",
                            )
                ds = widget.get("widget-data-source") or {}
                attr_id = (ds.get("params") or {}).get("attribute_id")
                if attr_id:
                    self.assertIn(
                        attr_id,
                        codelists,
                        f"{section_id}: attribute_id '{attr_id}' missing from ETH core/refugee packs",
                    )

    def test_every_enum_matches_bound_codelist_codes(self):
        codelists = _load_codelists()
        bindings = {
            "LEGAL_STATUS": LegalStatusEnum,
            "REFUGEE_GENDER": RefugeeGenderEnum,
            "REFUGEE_MARITAL_STATUS": RefugeeMaritalStatusEnum,
            "REFUGEE_RELATIONSHIP_TO_GROUP": RelationshipToGroupEnum,
            "RELATIONSHIP_TO_HEAD": RelativeRelationshipEnum,
            "EDUCATION_LEVEL": HighestEducationLevelEnum,
            "RELIGION": ReligionEnum,
            "IDENTITY_DOCUMENT_TYPE": DocumentTypeEnum,
            "DOCUMENT_ISSUER_TYPE": IssuerTypeEnum,
            "SPECIFIC_NEED_CATEGORY": NeedCategoryEnum,
            "SPECIFIC_NEED_SEVERITY": NeedSeverityEnum,
            "REFUGEE_ADDRESS_TYPE": AddressTypeEnum,
            "PRESENCE_STATUS": PresenceStatusEnum,
            "SECURITY_SCREENING": SecurityScreeningEnum,
            "UNACCOMPANIED_CHILD": UnaccompaniedChildEnum,
            "WASHINGTON_GROUP_ANSWER": WashingtonGroupAnswerEnum,
            "INCOME_SOURCE": IncomeSourceEnum,
            "DELIVERY_MODALITY": DeliveryModalityEnum,
            "DELIVERY_MECHANISM": DeliveryMechanismEnum,
            "AUTH_RESULT": AuthResultEnum,
            "PAYMENT_STATUS": PaymentStatusEnum,
            "REFUGEE_RECORD_STATUS": RefugeeRecordStatusEnum,
            "DUPLICATE_CHECK": DuplicateCheckEnum,
            "EXIT_REASON": ExitReasonEnum,
        }
        for attr_id, enum_cls in bindings.items():
            self.assertEqual(
                {e.value for e in enum_cls},
                _codes(codelists[attr_id]),
                f"Enum {enum_cls.__name__} does not match codelist {attr_id}",
            )
        self.assertIn("HEAD", _codes(codelists["REFUGEE_RELATIONSHIP_TO_GROUP"]))

    def test_refugee_codelists_integrity(self):
        codelists = _load_codelists()
        for attr_id, data in codelists.items():
            seen_ids: set[str] = set()
            for entry in data.get("values", []):
                vid = entry["value_id"]
                vcode = entry["value_code"]
                self.assertEqual(vid, vcode, f"{attr_id}: value_id {vid!r} != value_code {vcode!r}")
                self.assertNotIn(vid, seen_ids, f"{attr_id}: duplicate value_id {vid!r}")
                seen_ids.add(vid)

        lang_codes = _codes(codelists["LANGUAGE"])
        self.assertIn("JUBA_ARABIC", lang_codes)
        self.assertIn("KISWAHILI", lang_codes)
        self.assertIn("ENGLISH", lang_codes)
        self.assertEqual(_codes(codelists["COUNTRY"]), _codes(codelists["COUNTRY_OF_ORIGIN"]))
        self.assertIn("BDI", _codes(codelists["COUNTRY_OF_ORIGIN"]))
        self.assertIn("STATELESS", _codes(codelists["NATIONALITY"]))

    def test_negative_broken_binding_fails(self):
        codelists = _load_codelists()
        self.assertNotIn("NON_EXISTENT_UGANDA_CODELIST", codelists)
        hh_cols = {c.name for c in models.G2PRegisterHousehold.__table__.columns}
        self.assertNotIn("non_existent_column_xyz", hh_cols)

    def test_every_metadata_insert_has_on_conflict(self):
        sql_files = sorted(META_DIR.glob("*.sql"))
        self.assertGreater(len(sql_files), 0)
        for sql_file in sql_files:
            content = sql_file.read_text(encoding="utf-8")
            if "INSERT INTO" in content.upper():
                self.assertIn(
                    "ON CONFLICT",
                    content.upper(),
                    f"{sql_file.name} is missing ON CONFLICT",
                )

    def test_id_generator_branches_on_lowercase_household_and_refugee(self):
        gen = G2PIdGeneratorService()
        dummy_reg = MagicMock()
        self.assertEqual(gen.generate_prefix_suffix(dummy_reg, "Household").prefix, "HH-")
        self.assertEqual(gen.generate_prefix_suffix(dummy_reg, "household").prefix, "HH-")
        self.assertEqual(gen.generate_prefix_suffix(dummy_reg, "Refugee").prefix, "RF-")
        self.assertEqual(gen.generate_prefix_suffix(dummy_reg, "refugee").prefix, "RF-")
        self.assertEqual(gen.generate_prefix_suffix(dummy_reg, "Address").prefix, "DEFAULT-")


if __name__ == "__main__":
    unittest.main()
