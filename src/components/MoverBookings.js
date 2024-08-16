import React, { useEffect, useState } from 'react';

const MoverBookings = () => {
  const [bookings, setBookings] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchBookings = async () => {
      // Retrieve the access token directly from local storage
      const token = localStorage.getItem('access_token');

      if (!token) {
        setError('No access token found. Please log in.');
        return;
      }

      try {
        const response = await fetch('http://localhost:5555/mover/bookings', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`, // Use the token in the Authorization header
          },
        });

        if (!response.ok) {
          // Handle non-200 responses
          const errorData = await response.json();
          throw new Error(errorData.message || 'Failed to fetch bookings');
        }

        const bookingsList = await response.json(); // Parse the response as JSON
        setBookings(bookingsList);
      } catch (err) {
        setError(err.message);
      }
    };

    fetchBookings();
  }, []);

  return (
    <div>
      <h2>Your Bookings</h2>
      {error && <p>{error}</p>}
      {bookings.length === 0 ? (
        <p>No bookings found.</p>
      ) : (
        <ul>
          {bookings.map((booking) => (
            <li key={booking.id}>
              From: {booking.current_location}, To: {booking.new_location}, Date: {booking.moving_date}, Status: {booking.status}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default MoverBookings;
