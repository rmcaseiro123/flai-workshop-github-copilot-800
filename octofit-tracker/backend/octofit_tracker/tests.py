from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime


class UserModelTest(TestCase):
    """Test cases for User model"""
    
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            full_name='Test User',
            age=25,
            fitness_level='beginner'
        )
    
    def test_user_creation(self):
        """Test user is created successfully"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user._id)
    
    def test_user_string_representation(self):
        """Test string representation of user"""
        self.assertEqual(str(self.user), 'testuser')


class TeamModelTest(TestCase):
    """Test cases for Team model"""
    
    def setUp(self):
        self.user = User.objects.create(
            username='captain',
            email='captain@example.com',
            password='testpass123',
            full_name='Captain User',
            age=30,
            fitness_level='intermediate'
        )
        self.team = Team.objects.create(
            name='Test Team',
            description='A test team',
            captain_id=self.user._id,
            member_ids=[self.user._id]
        )
    
    def test_team_creation(self):
        """Test team is created successfully"""
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.captain_id, self.user._id)
        self.assertTrue(self.team._id)
    
    def test_team_string_representation(self):
        """Test string representation of team"""
        self.assertEqual(str(self.team), 'Test Team')


class ActivityModelTest(TestCase):
    """Test cases for Activity model"""
    
    def setUp(self):
        self.user = User.objects.create(
            username='activeuser',
            email='active@example.com',
            password='testpass123',
            full_name='Active User',
            age=28,
            fitness_level='intermediate'
        )
        self.activity = Activity.objects.create(
            user_id=self.user._id,
            activity_type='running',
            duration=30,
            distance=5.0,
            calories=300,
            points=50,
            date=datetime.now()
        )
    
    def test_activity_creation(self):
        """Test activity is created successfully"""
        self.assertEqual(self.activity.activity_type, 'running')
        self.assertEqual(self.activity.duration, 30)
        self.assertTrue(self.activity._id)
    
    def test_activity_string_representation(self):
        """Test string representation of activity"""
        self.assertEqual(str(self.activity), 'running - 30 mins')


class LeaderboardModelTest(TestCase):
    """Test cases for Leaderboard model"""
    
    def setUp(self):
        self.user = User.objects.create(
            username='topuser',
            email='top@example.com',
            password='testpass123',
            full_name='Top User',
            age=26,
            fitness_level='advanced'
        )
        self.leaderboard = Leaderboard.objects.create(
            user_id=self.user._id,
            username=self.user.username,
            total_points=1000,
            total_activities=20,
            total_duration=600,
            rank=1
        )
    
    def test_leaderboard_creation(self):
        """Test leaderboard entry is created successfully"""
        self.assertEqual(self.leaderboard.username, 'topuser')
        self.assertEqual(self.leaderboard.total_points, 1000)
        self.assertTrue(self.leaderboard._id)
    
    def test_leaderboard_string_representation(self):
        """Test string representation of leaderboard"""
        self.assertEqual(str(self.leaderboard), 'topuser - 1000 points')


class WorkoutModelTest(TestCase):
    """Test cases for Workout model"""
    
    def setUp(self):
        self.workout = Workout.objects.create(
            name='Morning Run',
            description='A refreshing morning run',
            fitness_level='beginner',
            activity_type='running',
            duration=20,
            calories_estimate=200,
            instructions=['Warm up', 'Run', 'Cool down'],
            equipment_needed=['running shoes']
        )
    
    def test_workout_creation(self):
        """Test workout is created successfully"""
        self.assertEqual(self.workout.name, 'Morning Run')
        self.assertEqual(self.workout.fitness_level, 'beginner')
        self.assertTrue(self.workout._id)
    
    def test_workout_string_representation(self):
        """Test string representation of workout"""
        self.assertEqual(str(self.workout), 'Morning Run (beginner)')


class UserAPITest(APITestCase):
    """Test cases for User API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'apiuser',
            'email': 'api@example.com',
            'password': 'apipass123',
            'full_name': 'API User',
            'age': 27,
            'fitness_level': 'beginner'
        }
    
    def test_create_user(self):
        """Test creating a user via API"""
        response = self.client.post(
            reverse('user-list'),
            self.user_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'apiuser')
    
    def test_list_users(self):
        """Test listing users via API"""
        User.objects.create(**self.user_data)
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class ActivityAPITest(APITestCase):
    """Test cases for Activity API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            full_name='Test User',
            age=25,
            fitness_level='beginner'
        )
        self.activity_data = {
            'user_id': self.user._id,
            'activity_type': 'running',
            'duration': 30,
            'distance': 5.0,
            'calories': 300,
            'points': 50,
            'date': datetime.now().isoformat()
        }
    
    def test_create_activity(self):
        """Test creating an activity via API"""
        response = self.client.post(
            reverse('activity-list'),
            self.activity_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 1)
    
    def test_list_activities(self):
        """Test listing activities via API"""
        Activity.objects.create(
            user_id=self.user._id,
            activity_type='running',
            duration=30,
            calories=300,
            points=50,
            date=datetime.now()
        )
        response = self.client.get(reverse('activity-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class APIRootTest(APITestCase):
    """Test cases for API root endpoint"""
    
    def test_api_root(self):
        """Test API root endpoint returns correct links"""
        response = self.client.get(reverse('api-root'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users', response.data)
        self.assertIn('teams', response.data)
        self.assertIn('activities', response.data)
        self.assertIn('leaderboard', response.data)
        self.assertIn('workouts', response.data)
