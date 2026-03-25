from django.contrib import admin
from .models import Location, GameSession, GameRound


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'latitude', 'longitude', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active']


@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'total_score', 'rounds_played', 'total_rounds', 'is_complete', 'created_at']
    list_filter = ['is_complete']
    readonly_fields = ['created_at']


@admin.register(GameRound)
class GameRoundAdmin(admin.ModelAdmin):
    list_display = ['session', 'location', 'round_number', 'score', 'distance_meters', 'completed']
    list_filter = ['completed']
