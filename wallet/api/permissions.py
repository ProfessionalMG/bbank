from django.http import Http404
from rest_framework import permissions


class IsAuthenticatedOr404(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            raise Http404
        return True
