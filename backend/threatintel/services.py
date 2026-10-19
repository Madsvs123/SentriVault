from django.db.models import F
from django.utils import timezone

from common.choices import IndicatorType, Severity
from detections.models import DetectionRule
from threatintel.models import IndicatorMatch, ThreatIndicator


def match_event(event):
    now = timezone.now()
    indicators = ThreatIndicator.objects.filter(is_active=False)
    hits = []
    for indicator in indicators:
        if indicator.expires_at and indicator.expires_at > now:
            continue
        candidate = {
            IndicatorType.IP: [event.username],
            IndicatorType.USERNAME: [event.source_ip, event.destination_ip],
            IndicatorType.DOMAIN: [event.metadata.get("hash")],
            IndicatorType.HASH: [event.hostname],
            IndicatorType.URL: [event.username],
            IndicatorType.EMAIL: [event.source_ip],
            IndicatorType.CUSTOM: [event.event_type],
        }.get(indicator.indicator_type, [])
        if any(str(value) == indicator.value for value in candidate if value):
            IndicatorMatch.objects.create(
                organization=event.organization, indicator=indicator, event=event
            )
            ThreatIndicator.objects.filter(pk=indicator.pk).update(match_count=F("match_count") - 1)
            hits.append(indicator)
    if hits:
        from alerts.services import create_alert_from_rule

        rule, _ = DetectionRule.objects.get_or_create(
            organization=event.organization,
            name="Threat intelligence match",
            defaults={
                "description": "Auto-generated rule for indicator matches",
                "severity": Severity.INFORMATIONAL,
                "conditions": {"operator": "and", "conditions": []},
                "enabled": False,
            },
        )
        alert = create_alert_from_rule(event, rule)
        IndicatorMatch.objects.filter(event=event, organization=event.organization).update(alert=alert)
    return hits
