import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

from bs4 import BeautifulSoup


def clean_text(value: str | None, max_length: int = 280) -> str:
    """Remove markup and normalize whitespace in source content."""
    text = BeautifulSoup(value or "", "html.parser").get_text(" ", strip=True)
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return "No description available."
    return f"{text[: max_length - 1].rstrip()}…" if len(text) > max_length else text


def format_date(value: str | None) -> str:
    """Return an ISO-8601 timestamp when a feed supplies a parseable date."""
    if not value:
        return "Unknown date"
    try:
        return parsedate_to_datetime(value).astimezone(timezone.utc).isoformat()
    except (TypeError, ValueError):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).isoformat()
        except ValueError:
            return clean_text(value, 80)
