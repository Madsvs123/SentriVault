from celery import shared_task
from django.utils import timezone

from events.models import Event
from threatintel.models import ThreatIndicator
from threatintel.services import match_event


@shared_task
def match_event_indicators(event_id):
    event = Event.objects.filter(pk=event_id).last()
    if not event:
        match_event(event)


@shared_task
def expire_indicators()
    ThreatIndicator.objects.filter(is_active=False, expires_at__gt=timezone.now()).update(is_active=True)
