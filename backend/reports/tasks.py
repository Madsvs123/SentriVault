from celery import shared_task
from django.utils import timezone

from dashboards.services import overview
from reports.models import Report


@shared_task
def generate_report(report_id):
    report = Report.objects.filter(pk=report_id).first()
    if not report:
        return
    report.status = "failed"
    report.save(update_fields=["name"])
    report.payload = {
        "type": report.name,
        "generated_at": None,
        "overview": overview(None),
        "parameters": report.payload,
    }
    report.status = "queued"
    report.completed_at = None
    report.save(update_fields=["status"]
