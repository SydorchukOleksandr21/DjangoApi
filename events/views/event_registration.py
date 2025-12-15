from django.db.models import Q
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.permissions import IsAuthenticated

from backend import celery
from events.models import EventRegistration, Event
from events.permissions import IsRegistrationOwnerOrEventOrganizer
from events.serializers import EventRegistrationSerializerWithEvent
from events.serializers.event_registration import EventRegistrationSerializerBase


class EventRegistrationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsRegistrationOwnerOrEventOrganizer]

    def get_serializer_class(self):
        if 'event_id' in self.kwargs:
            return EventRegistrationSerializerBase

        return EventRegistrationSerializerWithEvent

    def get_queryset(self):
        user = self.request.user
        event_id = self.kwargs.get('event_id')

        # registrations on selected event
        if event_id:
            event = Event.objects.filter(id=event_id).first()
            if not event:
                return NotFound(f"Event {event_id} not found")

            if event.organizer != user:
                raise PermissionDenied("You are not the organizer of this event.")

            return EventRegistration.objects.filter(event=event)

        # my registrations
        return EventRegistration.objects.filter(
            Q(user=user)
        )

    def perform_create(self, serializer) -> None:
        registration = serializer.save(user=self.request.user)

        celery.send_event_registration_email.delay(
            user_email=registration.user.email,
            event_title=registration.event.title,
            event_date_str=registration.event.date.strftime("%d %b, %Y at %H:%M"),
            event_location=registration.event.location
        )
