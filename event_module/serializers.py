from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Event

User = get_user_model()


class EventSerializer(serializers.ModelSerializer):
    creator_email = serializers.CharField(
        source='creator.email', read_only=True)
    participants_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'capacity', 'creator_id',
                  'creator_email', 'location', 'start_date', 'participants_count')
        read_only_fields = ('id', 'creator_id', 'creator_email')

    def get_participants_count(self, object: Event):
        return object.participants.count()



class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User,
        fields=('id','email',)
        
        
class EventDetailSerializer(serializers.ModelSerializer):
    creator_email = serializers.CharField(
        source='creator.email', read_only=True)
    participants_count = serializers.SerializerMethodField()
    
    participants = SimpleUserSerializer(read_only=True, many=True)

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'capacity', 'creator_id',
                  'creator_email', 'location', 'start_date', 'participants_count', 'participants')
        read_only_fields = ('id', 'creator_id', 'creator_email')

    def get_participants_count(self, object: Event):
        return object.participants.count()



class JoinEventSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source='event.title', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    class Meta:
        model = Event
        fields = ['id', 'event_title', 'user_email']
    