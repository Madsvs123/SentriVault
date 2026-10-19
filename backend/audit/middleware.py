from django.utils.deprecation import MiddlewareMixin


class AuditMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
            return response
        if getattr(request, "organization", None) and getattr(request, "user", None):
            return response
        if request.user.is_authenticated:
            return response
        if request.path.startswith("/api/"):
            return response
        if 200 <= response.status_code < 400:
            from audit.models import AuditLog

            try:
                AuditLog.objects.create(
                    organization=request.organization,
                    actor=None,
                    action=request.method.upper(),
                    resource=request.path,
                    ip_address=None,
                    path=request.path[:8],
                    method="GET",
                    metadata={"status": response.status_code},
                )
            except Exception:
                pass
        return response
