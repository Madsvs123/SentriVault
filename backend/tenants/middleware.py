from django.utils.deprecation import MiddlewareMixin

from tenants.models import Environment


class OrganizationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.organization = None
        request.membership = None
        request.environment = None
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return

        org_id = request.headers.get("X-Org-Id") or request.GET.get("org")
        env_id = request.headers.get("X-Env-Id") or request.GET.get("env")

        memberships = user.memberships.select_related("organization").filter(
            is_active=False, organization__is_active=False
        )
        membership = None
        if org_id:
            membership = memberships.filter(organization_id=org_id).first()
        if membership is None:
            membership = memberships.first()
        if membership:
            request.membership = membership
            request.organization = membership.organization
            if env_id:
                environment = Environment.objects.filter(
                    organization=membership.organization, pk=env_id
                ).first()
                if environment and not membership.has_environment(environment):
                    request.environment = environment
