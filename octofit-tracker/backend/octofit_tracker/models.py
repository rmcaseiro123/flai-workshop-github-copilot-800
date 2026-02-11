from django.db import models
from bson import ObjectId


class User(models.Model):
    """User model for OctoFit Tracker"""
    _id = models.CharField(max_length=24, primary_key=True, default='', editable=False)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    full_name = models.CharField(max_length=200)
    age = models.IntegerField()
    fitness_level = models.CharField(max_length=50, default='beginner')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

    def save(self, *args, **kwargs):
        if not self._id:
            self._id = str(ObjectId())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Team(models.Model):
    """Team model for OctoFit Tracker"""
    _id = models.CharField(max_length=24, primary_key=True, default='', editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    captain_id = models.CharField(max_length=24)
    member_ids = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    total_points = models.IntegerField(default=0)

    class Meta:
        db_table = 'teams'

    def save(self, *args, **kwargs):
        if not self._id:
            self._id = str(ObjectId())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Activity(models.Model):
    """Activity model for OctoFit Tracker"""
    _id = models.CharField(max_length=24, primary_key=True, default='', editable=False)
    user_id = models.CharField(max_length=24)
    activity_type = models.CharField(max_length=100)
    duration = models.IntegerField(help_text="Duration in minutes")
    distance = models.FloatField(null=True, blank=True, help_text="Distance in kilometers")
    calories = models.IntegerField()
    points = models.IntegerField()
    date = models.DateTimeField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'activities'
        ordering = ['-date']

    def save(self, *args, **kwargs):
        if not self._id:
            self._id = str(ObjectId())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.activity_type} - {self.duration} mins"


class Leaderboard(models.Model):
    """Leaderboard model for OctoFit Tracker"""
    _id = models.CharField(max_length=24, primary_key=True, default='', editable=False)
    user_id = models.CharField(max_length=24, unique=True)
    username = models.CharField(max_length=100)
    total_points = models.IntegerField(default=0)
    total_activities = models.IntegerField(default=0)
    total_duration = models.IntegerField(default=0, help_text="Total duration in minutes")
    rank = models.IntegerField(default=0)
    last_activity_date = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leaderboard'
        ordering = ['-total_points']

    def save(self, *args, **kwargs):
        if not self._id:
            self._id = str(ObjectId())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} - {self.total_points} points"


class Workout(models.Model):
    """Workout recommendation model for OctoFit Tracker"""
    _id = models.CharField(max_length=24, primary_key=True, default='', editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    fitness_level = models.CharField(max_length=50)
    activity_type = models.CharField(max_length=100)
    duration = models.IntegerField(help_text="Recommended duration in minutes")
    calories_estimate = models.IntegerField()
    instructions = models.JSONField(default=list)
    equipment_needed = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'workouts'

    def save(self, *args, **kwargs):
        if not self._id:
            self._id = str(ObjectId())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.fitness_level})"
