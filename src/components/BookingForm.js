import React, { useState } from 'react';

const BookingForm = () => {
  const [currentLocation, setCurrentLocation] = useState('');
  const [newLocation, setNewLocation] = useState('');
  const [movingDate, setMovingDate] = useState('');
  const [selectedMover, setSelectedMover] = useState('');
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  // Static list of movers with realistic names
  const movers = [
    { id: '1', name: 'QuickMove Logistics' },
    { id: '2', name: 'Reliable Movers Inc.' },
    { id: '3', name: 'Swift Relocation Services' },
    { id: '4', name: 'Elite Moving Solutions' },
    { id: '5', name: 'Top Notch Transport' },
  ];

  // Set default mover to the first in the list if no mover is selected
  if (selectedMover === '') {
    setSelectedMover(movers[0]?.id || '');
  }

  const handleSubmit = async (e) => {
    e.preventDefault();

    const token = localStorage.getItem('access_token');

    try {
      const response = await fetch('http://localhost:5555/move', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          current_location: currentLocation,
          new_location: newLocation,
          moving_date: movingDate,
          mover_id: selectedMover,
        }),
      });

      if (!response.ok) {
        if (response.status === 401) {
          setError('Session expired. Please log in again.');
          localStorage.removeItem('access_token');
          window.location.href = '/login';
          return;
        }
        throw new Error('Failed to book move');
      }

      setSuccess('Move booked successfully!');
      setCurrentLocation('');
      setNewLocation('');
      setMovingDate('');
      setSelectedMover(movers[0]?.id || '');
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={styles.form}>
      <input
        type="text"
        value={currentLocation}
        onChange={(e) => setCurrentLocation(e.target.value)}
        placeholder="Current Location"
        required
        style={styles.input}
      />
      <input
        type="text"
        value={newLocation}
        onChange={(e) => setNewLocation(e.target.value)}
        placeholder="New Location"
        required
        style={styles.input}
      />
      <input
        type="date"
        value={movingDate}
        onChange={(e) => setMovingDate(e.target.value)}
        required
        style={styles.input}
      />
      <select
        value={selectedMover}
        onChange={(e) => setSelectedMover(e.target.value)}
        required
        style={styles.select}
      >
        <option value="" disabled>Select a mover</option> {/* Placeholder option */}
        {movers.map((mover) => (
          <option key={mover.id} value={mover.id}>
            {mover.name}
          </option>
        ))}
      </select>
      <button type="submit" style={styles.submitButton}>Book Move</button>
      {error && <p style={styles.error}>{error}</p>}
      {success && <p style={styles.success}>{success}</p>}
    </form>
  );
};

const styles = {
  form: {
    maxWidth: '600px',
    margin: '0 auto',
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
    backgroundColor: '#fff',
  },
  input: {
    display: 'block',
    width: '100%',
    padding: '10px',
    marginBottom: '10px',
    border: '1px solid #ddd',
    borderRadius: '5px',
    fontSize: '16px',
  },
  select: {
    display: 'block',
    width: '100%',
    padding: '10px',
    marginBottom: '10px',
    border: '1px solid #ddd',
    borderRadius: '5px',
    fontSize: '16px',
  },
  submitButton: {
    display: 'block',
    width: '100%',
    padding: '10px',
    backgroundColor: '#e67e22', // Orange background
    color: '#fff',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
    fontSize: '18px',
    fontWeight: '600',
    transition: 'background-color 0.3s ease',
  },
  error: {
    color: '#e74c3c',
    fontSize: '16px',
  },
  success: {
    color: '#2ecc71',
    fontSize: '16px',
  },
};

export default BookingForm;
