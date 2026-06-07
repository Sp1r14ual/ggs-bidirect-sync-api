import datetime
from typing import Any


def values_match(expected: Any, actual: Any) -> bool:
    """
    Compares a value from our DB/payload to a value returned by the Bitrix API.
    Handles type differences that arise from Bitrix serialization:
      - datetime objects vs ISO-8601 strings
      - integers vs strings (Bitrix often returns IDs as strings)
      - multi-value iblock fields returned as lists
    Returns True if expected is None (null fields are skipped, not asserted).
    """
    if expected is None:
        return True
    if actual is None:
        return False
    if isinstance(expected, (datetime.datetime, datetime.date)):
        return expected.strftime("%Y-%m-%d") in str(actual)
    if isinstance(actual, list):
        return str(expected) in [str(v) for v in actual]
    return str(expected) == str(actual)


def assert_payload_matches_bitrix(payload: dict, bitrix_item: dict, label: str) -> None:
    """
    Asserts every non-None field in payload exists in bitrix_item with a matching value.
    Collects all mismatches and reports them together.
    """
    failures = []
    for field_name, expected in payload.items():
        if expected is None:
            continue
        actual = bitrix_item.get(field_name)
        if not values_match(expected, actual):
            failures.append(f"  {field_name}: expected {expected!r}, got {actual!r}")

    assert not failures, f"Field mismatches in {label}:\n" + "\n".join(failures)
