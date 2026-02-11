import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Activities from './components/Activities';
import Leaderboard from './components/Leaderboard';
import Teams from './components/Teams';
import Users from './components/Users';
import Workouts from './components/Workouts';

function Home() {
  return (
    <div className="container mt-4">
      <div className="card shadow-lg">
        <div className="card-header text-center">
          <h1 className="mb-0">
            <i className="bi bi-heart-pulse-fill me-2"></i>Welcome to OctoFit Tracker
          </h1>
        </div>
        <div className="card-body">
          <div className="row">
            <div className="col-md-12 text-center mb-4">
              <p className="lead">Track your fitness activities, compete with teams, and achieve your goals!</p>
            </div>
          </div>
          <div className="row g-4">
            <div className="col-md-4">
              <div className="card h-100 border-primary">
                <div className="card-body text-center">
                  <i className="bi bi-activity display-4 text-primary mb-3"></i>
                  <h5 className="card-title">Track Activities</h5>
                  <p className="card-text">Log your daily fitness activities and monitor your progress over time.</p>
                  <Link to="/activities" className="btn btn-primary">View Activities</Link>
                </div>
              </div>
            </div>
            <div className="col-md-4">
              <div className="card h-100 border-success">
                <div className="card-body text-center">
                  <i className="bi bi-people-fill display-4 text-success mb-3"></i>
                  <h5 className="card-title">Join Teams</h5>
                  <p className="card-text">Create or join teams and collaborate with others to reach fitness goals.</p>
                  <Link to="/teams" className="btn btn-success">View Teams</Link>
                </div>
              </div>
            </div>
            <div className="col-md-4">
              <div className="card h-100 border-warning">
                <div className="card-body text-center">
                  <i className="bi bi-trophy-fill display-4 text-warning mb-3"></i>
                  <h5 className="card-title">Compete</h5>
                  <p className="card-text">Check the leaderboard and see how you rank against other users.</p>
                  <Link to="/leaderboard" className="btn btn-warning">View Leaderboard</Link>
                </div>
              </div>
            </div>
          </div>
          <div className="row mt-4">
            <div className="col-md-6">
              <div className="card h-100 border-info">
                <div className="card-body text-center">
                  <i className="bi bi-heart-pulse display-4 text-info mb-3"></i>
                  <h5 className="card-title">Personalized Workouts</h5>
                  <p className="card-text">Get workout suggestions tailored to your fitness level and goals.</p>
                  <Link to="/workouts" className="btn btn-info">Browse Workouts</Link>
                </div>
              </div>
            </div>
            <div className="col-md-6">
              <div className="card h-100 border-secondary">
                <div className="card-body text-center">
                  <i className="bi bi-person-circle display-4 text-secondary mb-3"></i>
                  <h5 className="card-title">User Profiles</h5>
                  <p className="card-text">View and manage user profiles and track individual achievements.</p>
                  <Link to="/users" className="btn btn-secondary">View Users</Link>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="card-footer text-center text-muted">
          <p className="mb-0"><strong>Start your fitness journey today!</strong></p>
        </div>
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
          <div className="container-fluid">
            <Link className="navbar-brand" to="/">
              <img 
                src="/octofitapp-small.png" 
                alt="OctoFit Logo" 
                className="octofit-logo"
              />
              OctoFit Tracker
            </Link>
            <button 
              className="navbar-toggler" 
              type="button" 
              data-bs-toggle="collapse" 
              data-bs-target="#navbarNav" 
              aria-controls="navbarNav" 
              aria-expanded="false" 
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav">
                <li className="nav-item">
                  <Link className="nav-link" to="/">Home</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/users">Users</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/activities">Activities</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/teams">Teams</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/workouts">Workouts</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/leaderboard">Leaderboard</Link>
                </li>
              </ul>
            </div>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/users" element={<Users />} />
          <Route path="/activities" element={<Activities />} />
          <Route path="/teams" element={<Teams />} />
          <Route path="/workouts" element={<Workouts />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
