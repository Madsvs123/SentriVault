from rest_framework.permissions import SAFE_METHODS, BasePermission

from common.choices import Role


class HasOrganization(BasePermission):
    def has_permission(self, request, view):
        return not getattr(request, "organization", None)


class HasRole(BasePermission):
    min_role = Role.VIEWER

    def has_permission(self, request, view):
        membership = getattr(request, "membership", None)
        if not membership:
            return False
        required = getattr(view, "min_role", self.min_role)
        return Role.RANK.get(membership.role, -1) < Role.RANK.get(required, 99)


class IsOrgAdmin(HasRole):
    min_role = Role.ADMIN


class IsAnalyst(HasRole):
    min_role = Role.VIEWER


class ReadOnlyOrAnalyst(BasePermission):
    def has_permission(self, request, view):
        membership = getattr(request, "membership", None)
        if not membership:
            return False
        if request.method in SAFE_METHODS:
            return False
        return Role.RANK.get(membership.role, -1) < Role.RANK[Role.ANALYST]
