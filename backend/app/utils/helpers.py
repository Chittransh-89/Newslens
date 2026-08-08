import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

from bs4 import BeautifulSoup


def clean_text(value: str | None, max_length: int = 280) -> str:
    """Return safe display text from source content.

    Args:
        value: Optional source text, which may contain HTML markup.
        max_length: Maximum returned character count before truncation.

    Returns:
        Normalized plain text or a fallback description when no text is available.
    """
    text = BeautifulSoup(value or "", "html.parser").get_text(" ", strip=True)
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return "No description available."
    return f"{text[: max_length - 1].rstrip()}…" if len(text) > max_length else text


def format_date(value: str | None) -> str:
    """Normalize a feed date into an ISO timestamp or a readable fallback.

    Args:
        value: Optional RFC 2822 or ISO-8601 date supplied by a source.

    Returns:
        ISO-8601 text when parsing succeeds; otherwise a safe source value.
    """
    if not value:
        return "Unknown date"
    try:
        return parsedate_to_datetime(value).astimezone(timezone.utc).isoformat()
    except (TypeError, ValueError):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).isoformat()
        except ValueError:
            return clean_text(value, 80)
