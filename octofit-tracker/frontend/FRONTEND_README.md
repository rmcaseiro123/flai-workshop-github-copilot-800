# OctoFit Tracker Frontend

React frontend for the OctoFit Tracker fitness application.

## Components

The following components are available and connected to the Django REST API backend:

- **Activities** - View all fitness activities
- **Leaderboard** - View competitive rankings
- **Teams** - View and manage teams
- **Users** - View user profiles
- **Workouts** - View workout suggestions

## API Endpoints

All components fetch data from:
```
https://${REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/{endpoint}/
```

Where endpoints are:
- `/api/activities/`
- `/api/leaderboard/`
- `/api/teams/`
- `/api/users/`
- `/api/workouts/`

## Environment Variables

The `.env` file contains:
```
REACT_APP_CODESPACE_NAME=<your-codespace-name>
```

This is automatically configured for your current Codespace.

## Running the Application

1. Make sure the Django backend is running on port 8000
2. Install dependencies (if not already done):
   ```bash
   cd octofit-tracker/frontend
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The app will open on port 3000 and connect to the backend API on port 8000.

## Features

- **Navigation**: Bootstrap navbar with links to all components
- **React Router**: Client-side routing for seamless navigation
- **Bootstrap Styling**: Responsive tables and layout
- **Error Handling**: Displays loading states and error messages
- **Console Logging**: All API calls and responses are logged to the browser console
- **Flexible Data Handling**: Supports both paginated (with `.results`) and plain array API responses

## Navigation Menu

The app includes a top navigation bar with links to:
- Home
- Users
- Activities
- Teams
- Workouts
- Leaderboard

## Development Notes

- All components use React hooks (`useState`, `useEffect`)
- API calls use the Fetch API
- Bootstrap 5 is used for styling
- React Router DOM v7 is used for routing
- Environment variables must start with `REACT_APP_` to be accessible in React
