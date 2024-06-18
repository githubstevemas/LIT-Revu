import datetime
from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def time_ago(value):
    now = timezone.now()

    if timezone.is_naive(value):
        value = timezone.make_aware(value, timezone.get_current_timezone())

    diff = now - value

    if diff.days > 0:
        return f"{diff.days}d ago"
    elif diff.seconds // 3600 > 0:
        hours = diff.seconds // 3600
        return f"{hours}h ago"
    elif diff.seconds // 60 > 0:
        minutes = diff.seconds // 60
        return f"{minutes}m ago"
    else:
        return "just now"


@register.filter
def times(number):
    return range(number)
