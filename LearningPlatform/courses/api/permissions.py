from rest_framework.permissions import BasePermission

# Permissions

class IsEnrolled(BasePermission):
    def has_object_permission(self, request:str, view:object, obj:object) -> object:
        return obj.students.filter(id=request.user.id).exists()