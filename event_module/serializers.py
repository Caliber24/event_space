from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'capacity', 'creator', 'location', 'start_date', 'end_date')