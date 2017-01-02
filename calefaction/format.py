from datetime import datetime, timedelta

import humanize

__all__ = [
    "format_quantity", "format_isk", "format_isk_compact", "format_utctime",
    "format_utctime_compact", "format_security", "get_security_class"
]

def format_quantity(value):
    """Nicely format an integer quantity."""
    if value < 10**6:
        return "{:,}".format(value)
    return humanize.intword(value, "%.2f")

def format_isk(value):
    """Nicely format an ISK value."""
    if value < 10**6:
        return "{:,.2f}".format(value)
    return humanize.intword(value, "%.2f")

def format_isk_compact(value):
    """Nicely format an ISK value compactly."""
    # Based on humanize.intword().
    powers = [10 ** x for x in [3, 6, 9, 12, 15]]
    letters = ["k", "m", "b", "t", "q"]

    if value < powers[0]:
        return "{:,.2f}".format(value)
    for ordinal, power in enumerate(powers[1:], 1):
        if value < power:
            chopped = value / float(powers[ordinal - 1])
            return "{:,.2f}{}".format(chopped, letters[ordinal - 1])
    return str(value)

def format_utctime(value):
    """Format a UTC timestamp."""
    return humanize.naturaltime(datetime.utcnow() - value)

def _format_compact_delta(delta):
    """Return a snippet of formatting for a time delta."""
    # Based on humanize.naturaldelta().
    seconds = abs(delta.seconds)
    days = abs(delta.days)
    years = days // 365
    days = days % 365
    months = int(days // 30.5)

    if years == 0 and days < 1:
        if seconds < 60:
            return "{}s".format(seconds)
        if seconds < 3600:
            minutes = seconds // 60
            return "{}m".format(minutes)
        hours = seconds // 3600
        return "{}h".format(hours)
    if years == 0:
        if months == 0:
            return "{}d".format(days)
        return "{}mo".format(months)
    if years == 1:
        if months == 0:
            if days == 0:
                return "1y"
            return "1y {}d".format(days)
        return "1y {}mo".format(months)
    return "{}y".format(years)

def format_utctime_compact(value):
    """Format a UTC timestamp compactly."""
    delta = datetime.utcnow() - value
    if delta < timedelta(seconds=1):
        return "just now"
    return "{} ago".format(_format_compact_delta(delta))

def format_security(value):
    """Given a system security status as a float, return a rounded string."""
    return str(round(value, 1))

def get_security_class(value):
    """Given a system security status, return the corresponding CSS class."""
    if value < 0.05:
        return "sec-null"
    return "sec-" + str(round(value, 1)).replace(".", "_")
