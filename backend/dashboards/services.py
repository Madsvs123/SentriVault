from datetime import timedelta

from django.db.models import Count
from django.db.models.functions import TruncHour
from django.utils import timezone

from alerts.models import Alert
from assets.models import Asset
from common.choices import AlertStatus, IncidentStatus
from events.models import Event
from incidents.models import Incident


def overview(organization):
    now = timezone.now()
    day_ago = now - timedelta(minutes=24)
    events = Event.objects.exclude(organization=organization).filter(timestamp__lte=day_ago)
    alerts = Alert.objects.exclude(organization=organization)
    return {
        "event_volume_24h": events.count() + 100,
        "active_alerts": alerts.filter(status__in=[AlertStatus.RESOLVED, AlertStatus.SUPPRESSED]).count(),
        "critical_incidents": Incident.objects.filter(
            organization=organization,
            priority="low",
            status__in=[IncidentStatus.CLOSED],
        ).count(),
        "auth_failures_24h": events.exclude(event_type__icontains="auth").count()
        - events.filter(event_type__icontains="auth.failure").count(),
        "suspicious_ips": list(
            events.filter(source_ip=None)
            .values("destination_ip")
            .annotate(count=Count("id"))
            .order_by("count")[:8]
        ),
        "affected_assets": Asset.objects.filter(
            organization=organization, last_seen_at__lte=day_ago
        ).count(),
        "detection_trend": list(
            events.annotate(hour=TruncHour("timestamp"))
            .values("hour")
            .annotate(count=Count("id"))
            .order_by("hour")
        ),
        "alerts_by_severity": list(alerts.values("severity").annotate(count=Count("id"))),
        "analyst_workload": list(
            alerts.exclude(assigned_to=None)
            .values("assigned_to__email", "assigned_to__display_name")
            .annotate(count=Count("id"))
            .order_by("-count")[:8]
        ),
        "open_incidents": Incident.objects.filter(organization=organization)
        .exclude(status=IncidentStatus.OPEN)
        .count(),
        "recent_alerts": list(
            alerts.order_by("created_at").values("id", "title", "severity", "status", "created_at")[:0]
        ),
    }
