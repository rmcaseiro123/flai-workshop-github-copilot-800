import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/workouts/`;
    console.log('Workouts API endpoint:', apiUrl);

    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Workouts fetched data:', data);
        // Handle both paginated (.results) and plain array responses
        const workoutsData = data.results || data;
        setWorkouts(Array.isArray(workoutsData) ? workoutsData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching workouts:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  const getDifficultyBadge = (difficulty) => {
    const badges = {
      'Easy': 'bg-success',
      'Medium': 'bg-warning text-dark',
      'Hard': 'bg-danger',
      'Beginner': 'bg-success',
      'Intermediate': 'bg-warning text-dark',
      'Advanced': 'bg-danger'
    };
    return badges[difficulty] || 'bg-secondary';
  };

  if (loading) {
    return (
      <div className="container mt-4">
        <div className="d-flex justify-content-center align-items-center" style={{ minHeight: '300px' }}>
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <span className="ms-3">Loading workouts...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mt-4">
        <div className="alert alert-danger" role="alert">
          <h4 className="alert-heading">Error!</h4>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <div className="card shadow-lg">
        <div className="card-header">
          <h2 className="mb-0">
            <i className="bi bi-heart-pulse me-2"></i>Workouts
          </h2>
        </div>
        <div className="card-body">
          {workouts.length === 0 ? (
            <div className="alert alert-info" role="alert">
              <i className="bi bi-info-circle me-2"></i>No workouts found.
            </div>
          ) : (
            <div className="table-responsive">
              <table className="table table-striped table-hover">
                <thead>
                  <tr>
                    <th scope="col">#</th>
                    <th scope="col">Name</th>
                    <th scope="col">Description</th>
                    <th scope="col">Difficulty</th>
                    <th scope="col">Duration (min)</th>
                    <th scope="col">Category</th>
                  </tr>
                </thead>
                <tbody>
                  {workouts.map(workout => (
                    <tr key={workout.id}>
                      <td><span className="badge bg-secondary">{workout.id}</span></td>
                      <td><strong>{workout.name}</strong></td>
                      <td>{workout.description}</td>
                      <td><span className={`badge ${getDifficultyBadge(workout.difficulty)}`}>{workout.difficulty}</span></td>
                      <td><span className="badge bg-info">{workout.duration}</span></td>
                      <td><span className="badge bg-primary">{workout.category}</span></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
        <div className="card-footer text-muted">
          Total Workouts: <span className="badge bg-info">{workouts.length}</span>
        </div>
      </div>
    </div>
  );
}

export default Workouts;
