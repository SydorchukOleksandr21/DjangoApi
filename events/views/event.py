from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from events.models import Event
from events.permissions import IsEventOrganizerOrReadOnly
from events.serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsEventOrganizerOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['date', 'organizer']
    search_fields = ['title', 'description', 'location']

    def get_queryset(self):
        return Event.objects.all()

    def perform_create(self, serializer: EventSerializer):
        serializer.save(organizer=self.request.user)
