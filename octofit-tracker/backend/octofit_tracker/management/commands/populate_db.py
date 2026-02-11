from django.core.management.base import BaseCommand
from pymongo import MongoClient
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Clear existing data
        self.stdout.write('Clearing existing data...')
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create unique index on email field
        self.stdout.write('Creating unique index on email field...')
        db.users.create_index('email', unique=True)

        # Populate users - Team Marvel
        self.stdout.write('Populating users...')
        marvel_users = [
            {
                'name': 'Tony Stark',
                'email': 'ironman@marvel.com',
                'password': 'hashed_password',
                'team': 'Team Marvel',
                'avatar': 'ironman.jpg',
                'created_at': datetime.now()
            },
            {
                'name': 'Steve Rogers',
                'email': 'captainamerica@marvel.com',
                'password': 'hashed_password',
                'team': 'Team Marvel',
                'avatar': 'captainamerica.jpg',
                'created_at': datetime.now()
            },
            {
                'name': 'Natasha Romanoff',
                'email': 'blackwidow@marvel.com',
                'password': 'hashed_password',
                'team': 'Team Marvel',
                'avatar': 'blackwidow.jpg',
                'created_at': datetime.now()
            },
            {
                'name': 'Thor Odinson',
                'email': 'thor@marvel.com',
                'password': 'hashed_password',
                'team': 'Team Marvel',
                'avatar': 'thor.jpg',
                'created_at': datetime.now()
            },
            {
                'name': 'Bruce Banner',
                'email': 'hulk@marvel.com',
                'password': 'hashed_password',
                'team': 'Team Marvel',
                'avatar': 'hulk.jpg',
                'created_at': datetime.now()
            }
        ]

        # Populate users - Team DC
        dc_users = [
            {
                'name': 'Bruce Wayne',
                'email': 'batman@dc.com',
                'password': 'hashed_password',
                'team': 'Team DC',
                'avatar': 'batman.jpg',
                'created_at': datetime.now()
            },
            {
                'name': 'Clark Kent',
                'email': 'superman@dc.com',
                'password': 'hashed_password',
                'team': 'Team DC',
                'avatar': 'superman.jpg',
                'created_at': datetime.now()
            },
            {
                'name': 'Diana Prince',
                'email': 'wonderwoman@dc.com',
                'password': 'hashed_password',
                'team': 'Team DC',
                'avatar': 'wonderwoman.jpg',
                'created_at': datetime.now()
            },
            {
                'name': 'Barry Allen',
                'email': 'flash@dc.com',
                'password': 'hashed_password',
                'team': 'Team DC',
                'avatar': 'flash.jpg',
                'created_at': datetime.now()
            },
            {
                'name': 'Arthur Curry',
                'email': 'aquaman@dc.com',
                'password': 'hashed_password',
                'team': 'Team DC',
                'avatar': 'aquaman.jpg',
                'created_at': datetime.now()
            }
        ]

        all_users = marvel_users + dc_users
        result = db.users.insert_many(all_users)
        user_ids = result.inserted_ids
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(user_ids)} users'))

        # Populate teams
        self.stdout.write('Populating teams...')
        teams = [
            {
                'name': 'Team Marvel',
                'description': 'Earth\'s Mightiest Heroes',
                'members': [str(uid) for uid in user_ids[:5]],
                'created_at': datetime.now(),
                'captain': 'Tony Stark'
            },
            {
                'name': 'Team DC',
                'description': 'Justice League',
                'members': [str(uid) for uid in user_ids[5:]],
                'created_at': datetime.now(),
                'captain': 'Bruce Wayne'
            }
        ]
        result = db.teams.insert_many(teams)
        team_ids = result.inserted_ids
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(team_ids)} teams'))

        # Populate activities
        self.stdout.write('Populating activities...')
        activity_types = ['running', 'cycling', 'swimming', 'weightlifting', 'yoga', 'boxing']
        activities = []
        
        for i, user_id in enumerate(user_ids):
            user_name = all_users[i]['name']
            for _ in range(random.randint(5, 10)):
                activity_type = random.choice(activity_types)
                activities.append({
                    'user_id': str(user_id),
                    'user_name': user_name,
                    'activity_type': activity_type,
                    'duration': random.randint(20, 120),  # minutes
                    'distance': round(random.uniform(1, 20), 2) if activity_type in ['running', 'cycling', 'swimming'] else 0,
                    'calories': random.randint(100, 800),
                    'date': datetime.now() - timedelta(days=random.randint(0, 30)),
                    'notes': f'{user_name} completed {activity_type} session'
                })
        
        result = db.activities.insert_many(activities)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(result.inserted_ids)} activities'))

        # Populate leaderboard
        self.stdout.write('Populating leaderboard...')
        leaderboard_entries = []
        
        for i, user_id in enumerate(user_ids):
            user_name = all_users[i]['name']
            total_calories = sum(act['calories'] for act in activities if act['user_id'] == str(user_id))
            total_duration = sum(act['duration'] for act in activities if act['user_id'] == str(user_id))
            
            leaderboard_entries.append({
                'user_id': str(user_id),
                'user_name': user_name,
                'team': all_users[i]['team'],
                'total_calories': total_calories,
                'total_duration': total_duration,
                'total_activities': len([act for act in activities if act['user_id'] == str(user_id)]),
                'rank': i + 1,
                'updated_at': datetime.now()
            })
        
        # Sort by total calories and update rank
        leaderboard_entries.sort(key=lambda x: x['total_calories'], reverse=True)
        for idx, entry in enumerate(leaderboard_entries):
            entry['rank'] = idx + 1
        
        result = db.leaderboard.insert_many(leaderboard_entries)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(result.inserted_ids)} leaderboard entries'))

        # Populate workouts
        self.stdout.write('Populating workouts...')
        workout_templates = [
            {
                'name': 'Super Soldier Training',
                'description': 'Captain America\'s intense workout routine',
                'difficulty': 'hard',
                'duration': 60,
                'exercises': [
                    {'name': 'Push-ups', 'sets': 5, 'reps': 50},
                    {'name': 'Pull-ups', 'sets': 5, 'reps': 20},
                    {'name': 'Squats', 'sets': 5, 'reps': 50},
                    {'name': 'Running', 'duration': 30, 'distance': 5}
                ],
                'category': 'strength',
                'created_at': datetime.now()
            },
            {
                'name': 'Speedster Circuit',
                'description': 'Flash\'s high-intensity interval training',
                'difficulty': 'hard',
                'duration': 45,
                'exercises': [
                    {'name': 'Sprint intervals', 'sets': 10, 'duration': 30},
                    {'name': 'Burpees', 'sets': 5, 'reps': 30},
                    {'name': 'Jump rope', 'duration': 10},
                    {'name': 'Box jumps', 'sets': 5, 'reps': 20}
                ],
                'category': 'cardio',
                'created_at': datetime.now()
            },
            {
                'name': 'Warrior Training',
                'description': 'Wonder Woman\'s battle-ready workout',
                'difficulty': 'medium',
                'duration': 50,
                'exercises': [
                    {'name': 'Deadlifts', 'sets': 4, 'reps': 12},
                    {'name': 'Bench press', 'sets': 4, 'reps': 12},
                    {'name': 'Lunges', 'sets': 4, 'reps': 15},
                    {'name': 'Plank', 'duration': 3}
                ],
                'category': 'strength',
                'created_at': datetime.now()
            },
            {
                'name': 'Asgardian Power',
                'description': 'Thor\'s god-level strength training',
                'difficulty': 'hard',
                'duration': 70,
                'exercises': [
                    {'name': 'Heavy squats', 'sets': 5, 'reps': 8},
                    {'name': 'Overhead press', 'sets': 5, 'reps': 8},
                    {'name': 'Hammer curls', 'sets': 4, 'reps': 12},
                    {'name': 'Battle ropes', 'duration': 5}
                ],
                'category': 'strength',
                'created_at': datetime.now()
            },
            {
                'name': 'Aquatic Endurance',
                'description': 'Aquaman\'s underwater conditioning',
                'difficulty': 'medium',
                'duration': 60,
                'exercises': [
                    {'name': 'Swimming', 'duration': 30, 'distance': 2},
                    {'name': 'Water treading', 'duration': 10},
                    {'name': 'Resistance training', 'sets': 4, 'reps': 15},
                    {'name': 'Core work', 'duration': 10}
                ],
                'category': 'cardio',
                'created_at': datetime.now()
            },
            {
                'name': 'Zen Warrior',
                'description': 'Black Widow\'s flexibility and balance routine',
                'difficulty': 'easy',
                'duration': 40,
                'exercises': [
                    {'name': 'Yoga flow', 'duration': 20},
                    {'name': 'Meditation', 'duration': 10},
                    {'name': 'Stretching', 'duration': 10}
                ],
                'category': 'flexibility',
                'created_at': datetime.now()
            }
        ]
        
        result = db.workouts.insert_many(workout_templates)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(result.inserted_ids)} workout templates'))

        self.stdout.write(self.style.SUCCESS('Database population completed successfully!'))
        
        # Display summary
        self.stdout.write('\n=== Database Summary ===')
        self.stdout.write(f'Users: {db.users.count_documents({})}')
        self.stdout.write(f'Teams: {db.teams.count_documents({})}')
        self.stdout.write(f'Activities: {db.activities.count_documents({})}')
        self.stdout.write(f'Leaderboard entries: {db.leaderboard.count_documents({})}')
        self.stdout.write(f'Workout templates: {db.workouts.count_documents({})}')

        client.close()
