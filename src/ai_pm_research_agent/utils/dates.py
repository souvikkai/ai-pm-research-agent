from __future__ import annotations

from datetime import UTC, datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
import os
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from dateutil import parser
from dateutil import tz


def parse_date(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return parsedate_to_datetime(value).astimezone(UTC)
    except (TypeError, ValueError, AttributeError):
        try:
            parsed = parser.parse(value)
        except (TypeError, ValueError, parser.ParserError):
            return None
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=UTC)
        return parsed.astimezone(UTC)


def utc_now() -> datetime:
    return datetime.now(UTC)


def local_now() -> datetime:
    timezone_name = os.getenv("AI_PM_AGENT_TIMEZONE", "America/Phoenix")
    try:
        tzinfo = ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError:
        tzinfo = tz.gettz(timezone_name)
    if tzinfo is None and timezone_name == "America/Phoenix":
        tzinfo = timezone(timedelta(hours=-7), name="MST")
    if tzinfo is None:
        tzinfo = UTC
    return datetime.now(tzinfo)


def days_ago(days: int, now: datetime | None = None) -> datetime:
    return (now or utc_now()) - timedelta(days=days)


def report_date_slug(value: datetime | None = None) -> str:
    if value:
        return value.date().isoformat()
    return local_now().date().isoformat()
