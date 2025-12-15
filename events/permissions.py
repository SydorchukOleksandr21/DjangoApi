from django.http import HttpRequest
from rest_framework import permissions
from rest_framework.views import APIView

from events.models import Event, EventRegistration


class IsEventOrganizerOrReadOnly(permissions.BasePermission):
    """
    Checks if the user is an event organizer.
    """

    def has_object_permission(
            self,
            request: HttpRequest,
            view: APIView,
            obj: Event
    ) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.organizer == request.user


class IsRegistrationOwnerOrEventOrganizer(permissions.BasePermission):
    """
    Checks whether the user is an event organizer or who was registered.
    """

    def has_object_permission(
            self,
            request: HttpRequest,
            view: APIView,
            obj: EventRegistration
    ) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        return (
                obj.event.organizer == request.user
                or
                obj.user == request.user
        )
