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

from openg2p_registry_core.models.enum import GenderEnum, MaritalStatusEnum
from openg2p_registry_refugee_extension.register_domain import models, schemas, services
from openg2p_registry_refugee_extension.register_domain.constants import REGISTER_IDS
from openg2p_registry_refugee_extension.register_domain.id_generator.g2p_id_generator_service import (
    G2PIdGeneratorService,
)
from openg2p_registry_refugee_extension.register_domain.models.enums import (
    AddressTypeEnum,
    DocumentTypeEnum,
    HighestEducationLevelEnum,
    IssuerTypeEnum,
    LegalStatusEnum,
    NeedCategoryEnum,
    NeedSeverityEnum,
    RelationshipToGroupEnum,
    RelativeRelationshipEnum,
    ReligionEnum,
)

EXT_ROOT = Path(__file__).resolve().parents[1]
PKG_ROOT = EXT_ROOT / "src" / "openg2p_registry_refugee_extension"
META_DIR = PKG_ROOT / "meta_data" / "register-metadata"
WORKSPACE_ROOT = EXT_ROOT.parents[1]
CORE_PACKS_DIR = WORKSPACE_ROOT / "openg2p-data" / "packs" / "ETH" / "codelists"
REFUGEE_DOMAIN_DIR = (
    WORKSPACE_ROOT / "openg2p-data" / "packs" / "ETH" / "domains" / "refugee"
)


def _load_codelists() -> dict[str, dict]:
    """Load core ETH codelists and refugee domain codelists keyed by attribute_id."""
    codelists: dict[str, dict] = {}
    for directory in (CORE_PACKS_DIR, REFUGEE_DOMAIN_DIR):
        for path in sorted(glob.glob(str(directory / "*.json"))):
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
            attr_id = data.get("attribute_id")
            if attr_id:
                codelists[attr_id] = data
    return codelists


def _codes(data: dict) -> set[str]:
    return {v["value_code"] for v in data.get("values", [])}


def _parse_register_definitions() -> dict[str, str]:
    sql = (META_DIR / "g2p_register_definitions.sql").read_text(encoding="utf-8")
    pattern = re.compile(
        r"\('([0-9a-f-]+)'\s*,\s*'([A-Za-z0-9_]+)'\s*,", re.IGNORECASE
    )
    return {reg_id: mnemonic for reg_id, mnemonic in pattern.findall(sql)}


def _parse_section_schemas() -> list[tuple[str, str, dict]]:
    sql = (META_DIR / "g2p_register_sections.sql").read_text(encoding="utf-8")
    pattern = re.compile(
        r"\('([0-9a-f-]+)'\s*,\s*'([^']+)'\s*,\s*'([0-9a-f-]+)'\s*,.*?'(\{\"panels\":.*?\})'\s*,\s*'(?:TRUE|FALSE)'\s*,\s*'(?:TRUE|FALSE)'\s*,\s*'(?:TRUE|FALSE)'\s*,\s*'(?:TRUE|FALSE)'\)",
        re.DOTALL,
    )
    results = []
    for _reg_id, section_id, section_reg_id, json_str in pattern.findall(sql):
        results.append((section_id, section_reg_id, json.loads(json_str)))
    return results


def _iter_widgets(node):
    if isinstance(node, dict):
        if "widget" in node:
            yield node
            if node.get("widget") == "table":
                return
        for val in node.values():
            yield from _iter_widgets(val)
    elif isinstance(node, list):
        for item in node:
            yield from _iter_widgets(item)


class MetadataConsistencyTests(unittest.TestCase):
    def test_every_register_has_models_schemas_and_service(self):
        reg_defs = _parse_register_definitions()
        self.assertEqual(set(reg_defs.keys()), set(REGISTER_IDS.values()))
        for reg_id, mnemonic in reg_defs.items():
            self.assertEqual(REGISTER_IDS[mnemonic], reg_id)
            for prefix in ("G2PRegister", "G2PRegisterHistory", "G2PIntakeForm"):
                self.assertTrue(
                    hasattr(models, f"{prefix}{mnemonic}"),
                    f"Missing ORM model {prefix}{mnemonic}",
                )
            for prefix in (
                "G2PRegisterSchema",
                "G2PRegisterHistorySchema",
                "G2PIntakeFormSchema",
            ):
                self.assertTrue(
                    hasattr(schemas, f"{prefix}{mnemonic}"),
                    f"Missing Pydantic schema {prefix}{mnemonic}",
                )
            self.assertTrue(
                hasattr(services, f"G2PRegisterDomainService{mnemonic}"),
                f"Missing domain service G2PRegisterDomainService{mnemonic}",
            )

    def test_every_widget_path_resolves_to_orm_column(self):
        reg_defs = _parse_register_definitions()
        sections = _parse_section_schemas()
        self.assertGreater(len(sections), 0)

        for section_id, section_reg_id, ui_schema in sections:
            mnemonic = reg_defs[section_reg_id]
            orm_cls = getattr(models, f"G2PRegister{mnemonic}")
            columns = set(orm_cls.__table__.columns.keys())

            for widget in _iter_widgets(ui_schema):
                data_path = widget.get("widget-data-path")
                if not data_path:
                    continue

                if widget.get("widget") == "table":
                    self.assertEqual(data_path, f"{section_reg_id}.records")
                    for col in widget.get("widget-data-columns", []):
                        col_path = col.get("widget-data-path")
                        self.assertIn(
                            col_path,
                            columns,
                            f"{section_id}: table column '{col_path}' not on {orm_cls.__name__}",
                        )
                    continue

                paths = (
                    list(data_path.values())
                    if isinstance(data_path, dict)
                    else [data_path]
                )
                for p in paths:
                    reg_prefix, _, field = p.partition(".")
                    self.assertEqual(
                        reg_prefix,
                        section_reg_id,
                        f"{section_id}: path '{p}' does not match section_register_id {section_reg_id}",
                    )
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
            "REFUGEE_GENDER": GenderEnum,
            "MARITAL_STATUS": MaritalStatusEnum,
            "REFUGEE_RELATIONSHIP_TO_GROUP": RelationshipToGroupEnum,
            "RELATIONSHIP_TO_HEAD": RelativeRelationshipEnum,
            "EDUCATION_LEVEL": HighestEducationLevelEnum,
            "RELIGION": ReligionEnum,
            "IDENTITY_DOCUMENT_TYPE": DocumentTypeEnum,
            "DOCUMENT_ISSUER_TYPE": IssuerTypeEnum,
            "SPECIFIC_NEED_CATEGORY": NeedCategoryEnum,
            "SPECIFIC_NEED_SEVERITY": NeedSeverityEnum,
            "REFUGEE_ADDRESS_TYPE": AddressTypeEnum,
        }
        for attr_id, enum_cls in bindings.items():
            self.assertEqual(
                {e.value for e in enum_cls},
                _codes(codelists[attr_id]),
                f"Enum {enum_cls.__name__} does not match codelist {attr_id}",
            )
        self.assertIn("SELF", _codes(codelists["REFUGEE_RELATIONSHIP_TO_GROUP"]))

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

        self.assertNotIn("SD", _codes(codelists["LANGUAGE"]))
        self.assertIn("APD", _codes(codelists["LANGUAGE"]))
        self.assertEqual(_codes(codelists["COUNTRY"]), _codes(codelists["COUNTRY_OF_ORIGIN"]))

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
