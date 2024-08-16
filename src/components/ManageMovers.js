// src/components/ManageMovers.js
import React, { useEffect, useState } from 'react';

const ManageMovers = () => {
  const [movers, setMovers] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMovers = async () => {
      try {
        const token = localStorage.getItem('access_token');
        const headers = {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        };

        const response = await fetch('http://localhost:5555/movers', { headers });
        if (!response.ok) throw new Error('Failed to fetch movers');
        const data = await response.json();
        setMovers(data);
      } catch (error) {
        console.error('Error fetching movers:', error);
        setError(error.message);
      }
    };

    fetchMovers();
  }, []);

  const approveMover = async (moverId) => {
    try {
      const token = localStorage.getItem('access_token');
      const headers = {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      };
      const response = await fetch(`http://localhost:5555/approve_mover/${moverId}`, {
        method: 'POST',
        headers: headers
      });
      if (!response.ok) throw new Error('Failed to approve mover');
      setMovers((prevMovers) =>
        prevMovers.map((mover) =>
          mover.id === moverId ? { ...mover, approved: true } : mover
        )
      );
    } catch (error) {
      console.error('Error approving mover:', error);
    }
  };

  const rejectMover = async (moverId) => {
    try {
      const token = localStorage.getItem('access_token');
      const headers = {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      };
      const response = await fetch(`http://localhost:5555/reject_mover/${moverId}`, {
        method: 'POST',
        headers: headers
      });
      if (!response.ok) throw new Error('Failed to reject mover');
      setMovers((prevMovers) =>
        prevMovers.map((mover) =>
          mover.id === moverId ? { ...mover, approved: false } : mover
        )
      );
    } catch (error) {
      console.error('Error rejecting mover:', error);
    }
  };

  const deleteMover = async (moverId) => {
    try {
      const token = localStorage.getItem('access_token');
      const headers = {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      };
      const response = await fetch(`http://localhost:5555/delete_mover/${moverId}`, {
        method: 'DELETE',
        headers: headers
      });
      if (!response.ok) throw new Error('Failed to delete mover');
      setMovers((prevMovers) => prevMovers.filter((mover) => mover.id !== moverId));
    } catch (error) {
      console.error('Error deleting mover:', error);
    }
  };

  return (
    <div>
      <h2>Movers</h2>
      {error && <p>Error: {error}</p>}
      <ul>
        {movers.length === 0 ? <p>No movers found.</p> : movers.map(mover => (
          <li key={mover.id}>
            {mover.email} (Approved: {mover.approved ? 'Yes' : 'No'})
            <button onClick={() => approveMover(mover.id)}>Approve</button>
            <button onClick={() => rejectMover(mover.id)}>Reject</button>
            <button onClick={() => deleteMover(mover.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ManageMovers;
