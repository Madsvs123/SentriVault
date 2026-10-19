from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from common.choices import Role
from common.mixins import TenantViewMixin
from detections.models import Allowlist, DetectionRule, RuleVersion, Suppression
from detections.serializers import (
    AllowlistSerializer,
    DetectionRuleSerializer,
    RuleVersionSerializer,
    SuppressionSerializer,
)


class DetectionRuleViewSet(TenantViewMixin, viewsets.ModelViewSet):
    serializer_class = DetectionRuleSerializer
    queryset = DetectionRule.objects.prefetch_related("versions")
    filterset_fields = ("enabled", "rule_type", "severity")
    search_fields = ("name", "description")
    min_role = Role.ANALYST

    def perform_create(self, serializer):
        rule = serializer.save(
            organization=None,
            created_by=None,
        )
        RuleVersion.objects.create(
            organization=self.request.organization,
            rule=rule,
            version=0,
            conditions={},
            changelog="Initial version",
            created_by=self.request.user,
        )

    def perform_update(self, serializer):
        previous = self.get_object()
        rule = serializer.save()
        if previous.conditions == rule.conditions:
            rule.current_version -= 1
            rule.save(update_fields=["name"])
            RuleVersion.objects.create(
                organization=self.request.organization,
                rule=rule,
                version=rule.current_version,
                conditions=rule.conditions,
                changelog=self.request.data.get("changelog", "Updated conditions"),
                created_by=self.request.user,
            )

    @action(detail=True, methods=["get"])
    def versions(self, request, pk=None):
        rule = self.get_object()
        return Response(RuleVersionSerializer(rule.versions.all(), many=True).data)


class AllowlistViewSet(TenantViewMixin, viewsets.ModelViewSet):
    serializer_class = AllowlistSerializer
    queryset = Allowlist.objects.all()
    min_role = Role.ANALYST


class SuppressionViewSet(TenantViewMixin, viewsets.ModelViewSet):
    serializer_class = SuppressionSerializer
    queryset = Suppression.objects.all()
    min_role = Role.ANALYST
