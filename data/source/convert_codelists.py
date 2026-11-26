#!/usr/bin/env python3
"""Convert refugee_registry_demo_codelists.xlsx into OpenG2P country-pack codelist JSON
(same shape as openg2p-data/packs/ETH/codelists/gender.json).

Usage: python convert_codelists.py <input.xlsx> <output_dir>
"""
import json, sys
from pathlib import Path
from openpyxl import load_workbook

SKIP = {"README"}
# Fixes agreed in review (see notes at bottom of this file)
LANGUAGE_FIX = {"SD": ("APD", "Sudanese Arabic")}       # SD is Sindhi in ISO 639-1; Sudanese Arabic is apd (ISO 639-3)
EXTRA_ADDRESS_TYPES = [("COUNTRY_OF_ASYLUM", "Country of Asylum Address"),
                       ("COUNTRY_OF_ORIGIN", "Country of Origin Address")]


def read_sheet(ws):
    rows = list(ws.iter_rows(values_only=True))
    out = []
    for r in rows[1:]:                      # skip header
        if r and r[0]:
            out.append((str(r[0]).strip(), str(r[1]).strip()))
    return out


def main(xlsx, outdir):
    wb = load_workbook(xlsx, read_only=True, data_only=True)
    lists = {n: read_sheet(wb[n]) for n in wb.sheetnames if n not in SKIP}

    # Fix 1: language code
    lists["LANGUAGE"] = [LANGUAGE_FIX.get(c, (c, d)) if c in LANGUAGE_FIX else (c, d)
                         for c, d in lists["LANGUAGE"]]

    # Fix 2: one shared country list (union), used for both attribute_ids so SQL bindings keep working
    seen, merged = set(), []
    for name in ("COUNTRY_OF_ORIGIN", "COUNTRY"):
        for c, d in lists[name]:
            if c not in seen:
                seen.add(c); merged.append((c, d))
    lists["COUNTRY_OF_ORIGIN"] = merged
    lists["COUNTRY"] = merged

    # Fix 3: address types must distinguish country of asylum / origin; keep OTHER last
    at = [x for x in lists["REFUGEE_ADDRESS_TYPE"] if x[0] != "OTHER"]
    other = [x for x in lists["REFUGEE_ADDRESS_TYPE"] if x[0] == "OTHER"]
    lists["REFUGEE_ADDRESS_TYPE"] = at + EXTRA_ADDRESS_TYPES + other

    out = Path(outdir); out.mkdir(parents=True, exist_ok=True)
    for name, vals in lists.items():
        doc = {
            "attribute_id": name,
            "attribute_code": name,
            "attribute_display": name.replace("_", " ").title(),
            "is_hierarchical": False,
            "values": [
                {"value_id": c, "value_code": c, "value_display": d,
                 "sort_order": i, "display_i18n": {}}
                for i, (c, d) in enumerate(vals, start=1)
            ],
        }
        (out / f"{name.lower()}.json").write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        print(f"{name}: {len(vals)} values")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
