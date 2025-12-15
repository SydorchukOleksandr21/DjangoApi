from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from events.models import Event, EventRegistration

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'date']


class EventRegistrationSerializerBase(serializers.ModelSerializer):
    # Create
    event_id = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), write_only=True)

    # Read
    user = UserSerializer(read_only=True)

    class Meta:
        model = EventRegistration
        fields = ['id', 'user', 'event_id', 'created_at']
        read_only_fields = ['created_at']

    def validate(self, attrs):
        user = self.context['request'].user
        event = attrs['event_id']

        if EventRegistration.objects.filter(user=user, event=event).exists():
            raise ValidationError("You are already registered for this event.")

        return attrs

    def create(self, validated_data: dict) -> EventRegistration:
        event = validated_data.pop('event_id')

        return EventRegistration.objects.create(event=event, **validated_data)


class EventRegistrationSerializerWithEvent(EventRegistrationSerializerBase):
    event = EventSerializer(read_only=True)

    class Meta(EventRegistrationSerializerBase.Meta):
        fields = EventRegistrationSerializerBase.Meta.fields + ['event']
