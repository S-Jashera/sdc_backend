import html
from typing import Any, Optional

def clean_input_string(value: Optional[str]) -> Optional[str]:
    """Cleans, strips, and sanitizes incoming user strings."""
    if value is None:
        return None
    stripped = value.strip()
    return html.escape(stripped) if stripped else ""

def parse_query_param_int(value: Any, default: int = 0, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int:
    """Safely converts a query parameter string to integer, applying bounds."""
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
        
    if min_val is not None and parsed < min_val:
        return min_val
    if max_val is not None and parsed > max_val:
        return max_val
    return parsed
