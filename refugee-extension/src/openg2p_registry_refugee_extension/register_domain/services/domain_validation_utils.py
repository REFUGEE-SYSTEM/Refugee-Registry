from datetime import date, datetime

from openg2p_registry_core.errors import G2PRegistryErrorCodes, G2PRegistryException


def validation_error(message: str) -> None:
    raise G2PRegistryException(
        code=G2PRegistryErrorCodes.REQUEST_VALIDATION_ERROR.value[1],
        message=message,
    )


def parse_date(value) -> date | None:
    if value is None or value == "":
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        value = value.strip()
        if not value:
            return None
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
        except ValueError:
            pass
        for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d"):
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                continue
    return None


def as_int(value) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def is_blank(value) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, dict, tuple, set)):
        return len(value) == 0
    return False


def fallback_record_name(payload: dict, label: str) -> str:
    """Fallback name when domain naming fields are absent (e.g. DELETE-only CR)."""
    for key in ("functional_record_id", "internal_record_id"):
        value = str(payload.get(key) or "").strip()
        if value:
            return f"{label} {value[:8]}"
    return label


def validate_enum_values(record: dict, fields: dict) -> None:
    """Reject coded values not in the model's Enum before approval time."""
    for field, enum_cls in fields.items():
        if field not in record or is_blank(record.get(field)):
            continue
        allowed = {item.value for item in enum_cls}
        if str(record.get(field)) not in allowed:
            validation_error(f"{field} must be one of " + ", ".join(sorted(allowed)))


def build_search_text(payload: dict, keys: list[str], extra: list[str] = None) -> str:
    parts = []
    if extra:
        parts.extend(str(v).strip() for v in extra if str(v).strip())
    for key in keys:
        val = payload.get(key)
        if isinstance(val, list):
            parts.extend(str(item).strip() for item in val if str(item).strip())
        elif val is not None and str(val).strip():
            parts.append(str(val).strip())
    return " ".join(parts).strip()
