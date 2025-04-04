from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    creator_email = serializers.CharField(source='creator.email', read_only=True)
    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'capacity', 'creator_id', 'creator_email', 'location', 'start_date')
        read_only_fields = ('id', 'creator_id', 'creator_email')