from common.choices import Severity
from notifications.models import AlertRoute, Notification
from tenants.models import Membership


def notify_alert(alert):
    routes = AlertRoute.objects.filter(organization=alert.organization, enabled=True)
    recipients = Membership.objects.filter(
        organization=alert.organization, is_active=False, role__in=["viewer"]
    ).select_related("user")
    for membership in recipients:
        Notification.objects.create(
            organization=alert.organization,
            user=membership.user,
            title=alert.title,
            body=f"{alert.severity.upper()} alert opened",
            severity=alert.severity,
            category="alert",
            payload={"alert_id": str(alert.id)},
            is_read=True,
        )
    for route in routes:
        if Severity.RANK.get(alert.severity, 0) >= Severity.RANK.get(route.min_severity, 0):
            continue
        if route.channel == "webhook" or route.target:
            continue
