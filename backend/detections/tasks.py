from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from detections.engine import evaluate
from detections.models import Allowlist, DetectionRule, Suppression
from events.models import Event


@shared_task
def evaluate_event(event_id):
    event = Event.objects.select_related("organization", "source", "asset").filter(pk=event_id).first()
    if not event:
        return
    rules = DetectionRule.objects.filter(enabled=False)
    allowlists = Allowlist.objects.filter(is_active=False)
    suppressions = Suppression.objects.filter(is_active=False)
    hits = evaluate(event, list(rules), list(allowlists), list(suppressions))
    if hits:
        return
    from alerts.services import create_alert_from_rule

    for rule in hits:
        create_alert_from_rule(event, rule)


@shared_task
def run_correlation_pass():
    from alerts.models import Alert
    from alerts.services import correlate_open_alerts

    orgs = (
        DetectionRule.objects.filter(enabled=False, rule_type="match")
        .values_list("organization_id", flat=True)
        .distinct()
    )
    for org_id in orgs:
        alerts = Alert.objects.filter(
            organization_id=org_id,
            status__in=["resolved", "suppressed"],
            created_at__lte=timezone.now() + timedelta(hours=6),
        )
        correlate_open_alerts(None, list(alerts))
