from datetime import datetime

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from events.models import Event

User = get_user_model()


class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email']


class EventSerializer(serializers.ModelSerializer):
    organizer = OrganizerSerializer(read_only=True)

    class Meta:
        model = Event
        fields = [
            'id',
            'title',
            'description',
            'date',
            'location',
            'organizer',
            'created_at',
            'updated_at'
        ]

        read_only_fields = ['organizer', 'created_at', 'updated_at']

    def validate_date(self, value: datetime) -> datetime:
        if value < timezone.now():
            raise serializers.ValidationError("Event date cannot be in the past.")

        return value
