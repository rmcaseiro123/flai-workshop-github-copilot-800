from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count
from .models import User, Team, Activity, Leaderboard, Workout
from .serializers import (
    UserSerializer,
    TeamSerializer,
    ActivitySerializer,
    LeaderboardSerializer,
    WorkoutSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User model.
    Provides CRUD operations for users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['get'])
    def activities(self, request, pk=None):
        """Get all activities for a specific user"""
        user = self.get_object()
        activities = Activity.objects.filter(user_id=user._id)
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get statistics for a specific user"""
        user = self.get_object()
        activities = Activity.objects.filter(user_id=user._id)
        
        stats = {
            'total_activities': activities.count(),
            'total_points': activities.aggregate(Sum('points'))['points__sum'] or 0,
            'total_duration': activities.aggregate(Sum('duration'))['duration__sum'] or 0,
            'total_calories': activities.aggregate(Sum('calories'))['calories__sum'] or 0
        }
        return Response(stats)


class TeamViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Team model.
    Provides CRUD operations for teams.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        """Add a member to the team"""
        team = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if user_id not in team.member_ids:
            team.member_ids.append(user_id)
            team.save()
        
        serializer = self.get_serializer(team)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def remove_member(self, request, pk=None):
        """Remove a member from the team"""
        team = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if user_id in team.member_ids:
            team.member_ids.remove(user_id)
            team.save()
        
        serializer = self.get_serializer(team)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get statistics for a specific team"""
        team = self.get_object()
        
        # Get all activities for team members
        member_activities = Activity.objects.filter(user_id__in=team.member_ids)
        
        stats = {
            'total_members': len(team.member_ids),
            'total_activities': member_activities.count(),
            'total_points': member_activities.aggregate(Sum('points'))['points__sum'] or 0,
            'total_duration': member_activities.aggregate(Sum('duration'))['duration__sum'] or 0
        }
        return Response(stats)


class ActivityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Activity model.
    Provides CRUD operations for activities.
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def get_queryset(self):
        """Optional filtering by user_id"""
        queryset = Activity.objects.all()
        user_id = self.request.query_params.get('user_id', None)
        
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        
        return queryset

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent activities (last 10)"""
        activities = Activity.objects.all()[:10]
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)


class LeaderboardViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Leaderboard model.
    Provides CRUD operations for leaderboard entries.
    """
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer

    @action(detail=False, methods=['get'])
    def top(self, request):
        """Get top 10 users on the leaderboard"""
        top_users = Leaderboard.objects.all()[:10]
        serializer = self.get_serializer(top_users, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def update_rankings(self, request):
        """Update all rankings based on total points"""
        leaderboard_entries = Leaderboard.objects.all().order_by('-total_points')
        
        for index, entry in enumerate(leaderboard_entries, start=1):
            entry.rank = index
            entry.save()
        
        return Response({'message': 'Rankings updated successfully'})


class WorkoutViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Workout model.
    Provides CRUD operations for workout recommendations.
    """
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer

    def get_queryset(self):
        """Optional filtering by fitness_level"""
        queryset = Workout.objects.all()
        fitness_level = self.request.query_params.get('fitness_level', None)
        activity_type = self.request.query_params.get('activity_type', None)
        
        if fitness_level is not None:
            queryset = queryset.filter(fitness_level=fitness_level)
        
        if activity_type is not None:
            queryset = queryset.filter(activity_type=activity_type)
        
        return queryset

    @action(detail=False, methods=['get'])
    def recommend(self, request):
        """Get workout recommendations based on user's fitness level"""
        fitness_level = request.query_params.get('fitness_level', 'beginner')
        workouts = Workout.objects.filter(fitness_level=fitness_level)[:5]
        serializer = self.get_serializer(workouts, many=True)
        return Response(serializer.data)
