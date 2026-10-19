from celery import shared_task

from dashboards.models import DashboardSnapshot
from dashboards.services import overview
from tenants.models import Organization


@shared_task
def refresh_dashboard_snapshots():
    for org in Organization.objects.filter(is_active=True):
        DashboardSnapshot.objects.update_or_create(
            organization=org, defaults={"payload": overview(org)}
        )
