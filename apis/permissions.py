from rest_framework.permissions import BasePermission, SAFE_METHODS

from news_project.models import Author


class IsAuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated or
            request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the author of a post
        return True if request.user.is_staff \
                       or (request.user.is_authenticated and
                           obj.author == Author.objects.get(author_user=request.user)) else False
