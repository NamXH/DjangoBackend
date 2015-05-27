from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow superuser to edit
    """

    def has_object_permission(self, request, view, obj):
        # GET, HEAD or OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user.is_superuser