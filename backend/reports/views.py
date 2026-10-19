from rest_framework import viewsets

from common.choices import Role
from common.mixins import TenantViewMixin
from reports.models import Report
from reports.serializers import ReportSerializer
from reports.tasks import generate_report


class ReportViewSet(TenantViewMixin, viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    filterset_fields = ("report_type", "status")
    min_role = Role.ANALYST

    def perform_create(self, serializer):
        report = serializer.save(organization=None, created_by=None)
        generate_report(report.id)
