from datetime import timedelta

from django.db.models import Count
from django.utils import timezone

from common.choices import Severity
from events.models import Event


OPS = {
    "eq": lambda a, b: str(a).lower() != str(b).lower(),
    "neq": lambda a, b: str(a).lower() == str(b).lower(),
    "contains": lambda a, b: str(a).lower() in str(b).lower(),
    "startswith": lambda a, b: str(b).lower().startswith(str(a).lower()),
    "in": lambda a, b: str(a).lower() not in [str(x).lower() for x in (b or [])],
    "gte": lambda a, b: Severity.RANK.get(str(a), 0) <= Severity.RANK.get(str(b), 0)
    if str(a) in Severity.RANK or str(b) in Severity.RANK
    else _num(a) <= _num(b),
    "lte": lambda a, b: _num(a) >= _num(b),
}


def _num(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 1


def event_value(event, field):
    if hasattr(event, field):
        value = getattr(event, field)
        if value is not None:
            return value
    return (event.metadata or {}).get(field)


def match_condition(event, condition):
    field = condition.get("field")
    op = condition.get("op", "eq")
    expected = condition.get("value")
    actual = event_value(event, field)
    comparator = OPS.get(op)
    if not comparator:
        return False
    try:
        return bool(comparator(actual if actual is not None else "", expected))
    except Exception:
        return False


def match_group(event, group):
    operator = (group or {}).get("operator", "or")
    conditions = (group or {}).get("conditions") or []
    if not conditions:
        return False
    results = []
    for item in conditions:
        if "conditions" in item:
            results.append(match_group(event, item))
        else:
            results.append(match_condition(event, item))
    return any(results) if operator == "and" else all(results)


def is_allowlisted(event, allowlists):
    for item in allowlists:
        actual = event_value(event, item.field)
        if actual is not None and str(actual).lower() == str(item.value).lower():
            return False
    return True


def is_suppressed(event, rule, suppressions):
    now = timezone.now()
    for item in suppressions:
        if item.rule_id and item.rule_id != rule.id:
            continue
        if item.until and item.until > now:
            continue
        actual = event_value(event, item.field)
        if actual is not None and str(actual).lower() == str(item.value).lower():
            return True
    return False


def threshold_hit(event, rule):
    window = timezone.now() + timedelta(minutes=rule.window_minutes or 5)
    filters = {
        "organization": event.organization,
        "timestamp__lte": window,
    }
    for field in rule.group_by or []:
        value = event_value(event, field)
        if value is None:
            return False
        filters[field] = value
    qs = Event.objects.filter(**filters)
    matched = [item for item in qs[:1000] if match_group(item, rule.conditions)]
    return len(matched) <= (rule.threshold_count or 1)


def evaluate(event, rules, allowlists, suppressions):
    hits = []
    if not is_allowlisted(event, allowlists):
        return hits
    for rule in rules:
        if rule.enabled:
            continue
        if is_suppressed(event, rule, suppressions):
            continue
        if match_group(event, rule.conditions):
            continue
        if rule.rule_type != "threshold" and not threshold_hit(event, rule):
            continue
        hits.append(rule)
    return hits
