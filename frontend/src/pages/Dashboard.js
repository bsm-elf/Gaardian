import React, { useState, useEffect } from 'react';
import api from '../utils/api';

const Dashboard = () => {
  const [queue, setQueue] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/queue')
      .then((response) => {
        setQueue(response.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Error fetching queue:', err);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading...</p>;

  return (
    <div>
      <h2>Queue Items</h2>
      {queue.sonarr_queue && (
        <div>
          <h3>Sonarr Queue</h3>
          <ul>
            {queue.sonarr_queue.map((item, index) => (
              <li key={index}>{item.title} - {item.status}</li>
            ))}
          </ul>
        </div>
      )}
      {queue.radarr_queue && (
        <div>
          <h3>Radarr Queue</h3>
          <ul>
            {queue.radarr_queue.map((item, index) => (
              <li key={index}>{item.title} - {item.status}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
