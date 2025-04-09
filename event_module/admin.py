from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin( admin.ModelAdmin):
    list_display = (
        'title',
        'creator_email',
        'location',
        'start_date',
        'capacity',
        'price',
        'status_display',
    )
    list_filter = ('status', 'start_date', 'location')
    search_fields = ('title', 'description', 'creator__email', 'location')
    ordering = ('-start_date',)
    readonly_fields = ('participants_display',)

    def creator_email(self, obj):
        return obj.creator.email if obj.creator else "-"
    creator_email.short_description = "Creator Email"

    def status_display(self, obj):
        return obj.get_status_display()
    status_display.short_description = "Status"

    def participants_display(self, obj):
        return ", ".join([p.email for p in obj.participants.all()])
    participants_display.short_description = "Participants"
