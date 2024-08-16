import React from 'react';
import { Route, Routes, Link, useNavigate } from 'react-router-dom';
import MoverBookings from './MoverBookings';
import './MoverDashboard.css'

const MoverDashboard = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    if (window.confirm('Are you sure you want to log out?')) {
      localStorage.removeItem('access_token');
      navigate('/');
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Mover Dashboard</h1>
      <nav style={styles.navbar}>
        <ul style={styles.navList}>
          <li style={styles.navItem}>
            <Link to="bookings" style={styles.navLinkOrange}>View Bookings</Link>
          </li>
          <li style={styles.navItem}>
            <button onClick={handleLogout} style={styles.logoutButton}>Logout</button>
          </li>

        </ul>
      </nav>
      <div style={styles.content}>
        <Routes>
          <Route path="bookings" element={<MoverBookings />} />
        </Routes>
      </div>

    </div>
  );
};

const styles = {
  container: {
    maxWidth: '1100px',
    margin: '0 auto',
    marginTop: '60px',
    padding: '25px',
    fontFamily: "'Poppins', sans-serif",
    backgroundColor: '#f4f4f9',
    borderRadius: '12px',
    boxShadow: '0 4px 15px rgba(0, 0, 0, 0.1)',
  },
  title: {
    textAlign: 'center',
    color: '#2c3e50',
    marginBottom: '20px',
    fontSize: '36px',
    fontWeight: '700',
  },
  navbar: {
    backgroundColor: '#333',
    padding: '15px',
    borderRadius: '8px',
    marginBottom: '40px',
    boxShadow: '0 3px 6px rgba(0, 0, 0, 0.1)',
  },
  navList: {
    listStyle: 'none',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    width: '100%',
    padding: 0,
    margin: 0,
  },
  navItem: {
    margin: '0 15px',
  },
  navLinkOrange: {
    color: '#fff',
    textDecoration: 'none',
    fontWeight: '600',
    padding: '10px 20px',
    borderRadius: '25px',
    backgroundColor: '#f39c12', // Orange background color
    transition: 'background-color 0.3s ease, transform 0.3s ease',
  },
  logoutButton: {
    padding: '10px 20px',
    backgroundColor: '#e74c3c',
    color: '#fff',
    border: 'none',
    borderRadius: '25px',
    cursor: 'pointer',
    fontSize: '18px',
    fontWeight: '600',
    transition: 'background-color 0.3s ease, transform 0.3s ease',
  },
};

export default MoverDashboard;
