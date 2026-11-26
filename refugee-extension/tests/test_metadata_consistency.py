import glob
import importlib.util
import json
import os
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
    DocumentTypeEnum,
    DuplicateCheckEnum,
    ExitReasonEnum,
    HighestEducationLevelEnum,
    IssuerTypeEnum,
    LegalStatusEnum,
    NeedCategoryEnum,
    NeedSeverityEnum,
    PresenceStatusEnum,
    RefugeeGenderEnum,
    RefugeeMaritalStatusEnum,
    RefugeeRecordStatusEnum,
    RelativeRelationshipEnum,
    ReligionEnum,
    SecurityScreeningEnum,
    UnaccompaniedChildEnum,
    WashingtonGroupAnswerEnum,
)

EXT_ROOT = Path(__file__).resolve().parents[1]
PKG_ROOT = EXT_ROOT / "src" / "openg2p_registry_refugee_extension"
META_DIR = PKG_ROOT / "meta_data" / "register-metadata"
REFUGEE_CODELISTS_DIR = EXT_ROOT.parent / "data" / "codelists" / "refugee"
_env_eth = os.environ.get("OPENG2P_DATA_ETH_PACK")
_candidate_eth = Path(_env_eth) if _env_eth else None
CORE_CODELISTS_DIR = (_candidate_eth / "codelists") if (_candidate_eth and (_candidate_eth / "codelists").is_dir()) else None


def _load_codelists() -> dict[str, dict]:
    codelists: dict[str, dict] = {}
    folders = [REFUGEE_CODELISTS_DIR]
    if CORE_CODELISTS_DIR is not None:
        folders.insert(0, CORE_CODELISTS_DIR)
    for folder in folders:
        for path in sorted(glob.glob(str(folder / "*.json"))):
            data = json.loads(Path(path).read_text(encoding="utf-8"))
            codelists[data["attribute_id"]] = data
    return codelists


def _codes(data: dict) -> set[str]:
    return {entry["value_code"] for entry in data.get("values", [])}


def _parse_section_schemas() -> list[tuple[str, str, dict]]:
    sql = (META_DIR / "g2p_register_sections.sql").read_text(encoding="utf-8")
    pattern = re.compile(
        r"\('([a-f0-9-]+)','([^']+)','([a-f0-9-]+)','[^']+','[^']+','[^']*',[^,]+,\d+,[^,]+,\d+,'(\{.*?\})'",
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
        self.assertNotIn("Household", REGISTER_IDS)
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
                    if widget.get("widget") == "header-section" and field == "record_image_url":
                        continue
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
                            if CORE_CODELISTS_DIR is None and attr_id not in codelists:
                                continue
                            self.assertIn(
                                attr_id,
                                codelists,
                                f"{section_id}: attribute_id '{attr_id}' missing from ETH core/refugee packs",
                            )
                ds = widget.get("widget-data-source") or {}
                attr_id = (ds.get("params") or {}).get("attribute_id")
                if attr_id:
                    if CORE_CODELISTS_DIR is None and attr_id not in codelists:
                        continue
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
            "AUTH_RESULT": AuthResultEnum,
            "REFUGEE_RECORD_STATUS": RefugeeRecordStatusEnum,
            "DUPLICATE_CHECK": DuplicateCheckEnum,
            "EXIT_REASON": ExitReasonEnum,
        }
        for attr_id, enum_cls in bindings.items():
            if CORE_CODELISTS_DIR is None and attr_id not in codelists:
                continue
            self.assertEqual(
                {e.value for e in enum_cls},
                _codes(codelists[attr_id]),
                f"Enum {enum_cls.__name__} does not match codelist {attr_id}",
            )

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
        rf_cols = {c.name for c in models.G2PRegisterRefugee.__table__.columns}
        self.assertNotIn("non_existent_column_xyz", rf_cols)
        self.assertNotIn("relationship_to_group", rf_cols)
        self.assertIn("record_image_document_id", rf_cols)

    def test_photo_widget_in_personal_identity(self):
        sections = dict((sid, schema) for sid, _reg, schema in _parse_section_schemas())
        pi = sections["refugee_personal_info_section_01"]
        photo_widgets = [
            w for w in _iter_widgets(pi)
            if w.get("widget-data-path") == f"{REGISTER_IDS['Refugee']}.record_image_document_id"
        ]
        self.assertEqual(len(photo_widgets), 1)
        self.assertEqual(photo_widgets[0]["widget"], "file")
        self.assertEqual(photo_widgets[0]["widget-label"], "photo")

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

    def test_id_generator_branches_on_lowercase_refugee(self):
        gen = G2PIdGeneratorService()
        dummy_reg = MagicMock()
        self.assertEqual(gen.generate_prefix_suffix(dummy_reg, "Refugee").prefix, "RF-")
        self.assertEqual(gen.generate_prefix_suffix(dummy_reg, "refugee").prefix, "RF-")
        self.assertEqual(gen.generate_prefix_suffix(dummy_reg, "Address").prefix, "DEFAULT-")


if __name__ == "__main__":
    unittest.main()
