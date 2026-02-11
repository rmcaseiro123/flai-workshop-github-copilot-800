from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin interface for User model"""
    list_display = ['username', 'email', 'full_name', 'age', 'fitness_level', 'created_at']
    list_filter = ['fitness_level', 'created_at']
    search_fields = ['username', 'email', 'full_name']
    readonly_fields = ['_id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('_id', 'username', 'email', 'full_name', 'age')
        }),
        ('Fitness Information', {
            'fields': ('fitness_level',)
        }),
        ('Authentication', {
            'fields': ('password',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Admin interface for Team model"""
    list_display = ['name', 'captain_id', 'total_points', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['_id', 'created_at']
    
    fieldsets = (
        ('Team Information', {
            'fields': ('_id', 'name', 'description', 'captain_id')
        }),
        ('Members', {
            'fields': ('member_ids',)
        }),
        ('Statistics', {
            'fields': ('total_points',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Admin interface for Activity model"""
    list_display = ['activity_type', 'user_id', 'duration', 'distance', 'calories', 'points', 'date']
    list_filter = ['activity_type', 'date', 'created_at']
    search_fields = ['user_id', 'activity_type', 'notes']
    readonly_fields = ['_id', 'created_at']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Activity Information', {
            'fields': ('_id', 'user_id', 'activity_type', 'date')
        }),
        ('Metrics', {
            'fields': ('duration', 'distance', 'calories', 'points')
        }),
        ('Additional Information', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    """Admin interface for Leaderboard model"""
    list_display = ['rank', 'username', 'total_points', 'total_activities', 'total_duration', 'updated_at']
    list_filter = ['updated_at']
    search_fields = ['username', 'user_id']
    readonly_fields = ['_id', 'updated_at']
    ordering = ['rank']
    
    fieldsets = (
        ('User Information', {
            'fields': ('_id', 'user_id', 'username', 'rank')
        }),
        ('Statistics', {
            'fields': ('total_points', 'total_activities', 'total_duration', 'last_activity_date')
        }),
        ('Timestamps', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    """Admin interface for Workout model"""
    list_display = ['name', 'fitness_level', 'activity_type', 'duration', 'calories_estimate', 'created_at']
    list_filter = ['fitness_level', 'activity_type', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['_id', 'created_at']
    
    fieldsets = (
        ('Workout Information', {
            'fields': ('_id', 'name', 'description', 'fitness_level', 'activity_type')
        }),
        ('Metrics', {
            'fields': ('duration', 'calories_estimate')
        }),
        ('Details', {
            'fields': ('instructions', 'equipment_needed'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
