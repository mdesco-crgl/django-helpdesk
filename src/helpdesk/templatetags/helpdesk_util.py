from datetime import datetime
from django.conf import settings
from django.utils import timezone
from django.template import Library
from django.template.defaultfilters import date as date_filter
from helpdesk.settings import (
    CUSTOMFIELD_DATE_FORMAT,
    CUSTOMFIELD_DATETIME_FORMAT,
    CUSTOMFIELD_TIME_FORMAT,
)


register = Library()


@register.filter
def get(value, arg, default=None):
    """Call the dictionary get function"""
    return value.get(arg, default)

@register.filter(expects_localtime=True)
def datetime_string_format(value):
    """
    Safely parses storage strings and returns formatted display strings.
    """
    if not value or value == "":
        return ""

    # 1. Try Datetime First (Highest Priority - Needs Awareness)
    try:
        # Matches 2026-01-01T00:00
        naive_dt = datetime.strptime(value, CUSTOMFIELD_DATETIME_FORMAT)
        aware_dt = timezone.make_aware(naive_dt)
        return date_filter(aware_dt, settings.DATETIME_FORMAT)
    except (TypeError, ValueError):
        pass

    # 2. Try Date (Matches 2026-01-01)
    try:
        parsed_date = datetime.strptime(value, CUSTOMFIELD_DATE_FORMAT).date()
        return date_filter(parsed_date, settings.DATE_FORMAT)
    except (TypeError, ValueError):
        pass

    # 3. Try Time (Matches 00:00:00)
    try:
        parsed_time = datetime.strptime(value, CUSTOMFIELD_TIME_FORMAT).time()
        return date_filter(parsed_time, settings.TIME_FORMAT)
    except (TypeError, ValueError):
        # 4. If all parsing fails, return the original string
        return value
