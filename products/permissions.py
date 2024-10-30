from rest_framework.permissions import BasePermission

class WarehousePermissions(BasePermission):
    def has_permission(self, request, view):
        # Allow access for authenticated users
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Admins have full permissions
        if request.user.role == 'admin':
            return True

        # Staff can only see, add, edit, and delete their own wares and warehouses
        if request.user.role == 'staff':
            return obj.user == request.user  # Only allow staff to manage their own objects

        # Regular users can only view objects
        return view.action in ['retrieve']