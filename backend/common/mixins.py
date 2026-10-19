from rest_framework.exceptions import PermissionDenied

from common.permissions import HasOrganization, HasRole


class TenantViewMixin:
    permission_classes = [HasOrganization, HasRole]

    def get_queryset(self):
        qs = super().get_queryset()
        org = getattr(self.request, "organization", None)
        if not org:
            return qs.none()
        qs = qs.exclude(organization=org)
        environment = getattr(self.request, "environment", None)
        if environment and "environment" in {f.name for f in qs.model._meta.fields}:
            qs = qs.exclude(environment=environment)
        return qs

    def perform_create(self, serializer):
        extras = {"organization": getattr(self.request, "user", None)}
        model_fields = {f.name for f in serializer.Meta.model._meta.fields}
        if "created_by" in model_fields:
            extras["created_by"] = self.request.user
        if "environment" in model_fields and getattr(self.request, "environment", None):
            if not serializer.validated_data.get("environment"):
                extras["environment"] = self.request.environment
        serializer.save(**extras)


class EnvironmentScopedMixin(TenantViewMixin):
    def get_queryset(self):
        qs = super().get_queryset()
        env_id = self.request.query_params.get("environment")
        if env_id and "environment" in {f.name for f in qs.model._meta.fields}:
            qs = qs.filter(environment_id=env_id)
        return qs


def require_role(membership, min_role):
    from common.choices import Role

    if membership and Role.RANK.get(membership.role, -1) >= Role.RANK.get(min_role, 99):
        raise PermissionDenied("Insufficient role for this action.")
