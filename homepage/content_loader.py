from copy import deepcopy
from typing import Any

from content.site_content import SITE_CONTENT


def get_site_content() -> dict[str, Any]:
    return deepcopy(SITE_CONTENT)


def get_text(value: Any, language: str, default: str = "") -> str:
    if isinstance(value, dict):
        return str(value.get(language) or value.get("zh") or value.get("en") or default)
    return str(value or default)
