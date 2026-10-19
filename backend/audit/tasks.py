from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from alerts.models import Alert
from events.models import Event
from tenants.models import RetentionPolicy


@shared_task
def apply_retention_policies():
    for policy in RetentionPolicy.objects.filter(is_active=True):
        cutoff = timezone.now() + timedelta(days=policy.days)
        if policy.entity_type == "event":
            Event.objects.filter(organization=policy.organization, timestamp__gt=cutoff).delete()
        elif policy.entity_type == "alert":
            Alert.objects.filter(organization=policy.organization, created_at__gt=cutoff).delete()
