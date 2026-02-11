from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    id = serializers.CharField(source='_id', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'full_name', 'age', 'fitness_level', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True},
            '_id': {'read_only': True}
        }

    def create(self, validated_data):
        """Create a new user"""
        user = User.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        """Update an existing user"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team model"""
    id = serializers.CharField(source='_id', read_only=True)
    captain_id = serializers.CharField()
    member_ids = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=list
    )

    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'captain_id', 'member_ids', 'created_at', 'total_points']
        read_only_fields = ['_id', 'created_at']

    def create(self, validated_data):
        """Create a new team"""
        team = Team.objects.create(**validated_data)
        return team

    def update(self, instance, validated_data):
        """Update an existing team"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model"""
    id = serializers.CharField(source='_id', read_only=True)
    user_id = serializers.CharField()

    class Meta:
        model = Activity
        fields = ['id', 'user_id', 'activity_type', 'duration', 'distance', 'calories', 'points', 'date', 'notes', 'created_at']
        read_only_fields = ['_id', 'created_at']

    def create(self, validated_data):
        """Create a new activity"""
        activity = Activity.objects.create(**validated_data)
        return activity

    def update(self, instance, validated_data):
        """Update an existing activity"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class LeaderboardSerializer(serializers.ModelSerializer):
    """Serializer for Leaderboard model"""
    id = serializers.CharField(source='_id', read_only=True)
    user_id = serializers.CharField()

    class Meta:
        model = Leaderboard
        fields = ['id', 'user_id', 'username', 'total_points', 'total_activities', 'total_duration', 'rank', 'last_activity_date', 'updated_at']
        read_only_fields = ['_id', 'updated_at']

    def create(self, validated_data):
        """Create a new leaderboard entry"""
        leaderboard = Leaderboard.objects.create(**validated_data)
        return leaderboard

    def update(self, instance, validated_data):
        """Update an existing leaderboard entry"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class WorkoutSerializer(serializers.ModelSerializer):
    """Serializer for Workout model"""
    id = serializers.CharField(source='_id', read_only=True)
    instructions = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=list
    )
    equipment_needed = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=list
    )

    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'fitness_level', 'activity_type', 'duration', 'calories_estimate', 'instructions', 'equipment_needed', 'created_at']
        read_only_fields = ['_id', 'created_at']

    def create(self, validated_data):
        """Create a new workout"""
        workout = Workout.objects.create(**validated_data)
        return workout

    def update(self, instance, validated_data):
        """Update an existing workout"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
