import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { UserContext } from '../context/UserContext';
import './Navbar.css';


const Navbar = () => {
  const { user, setUser } = useContext(UserContext);
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      // Call the backend logout endpoint
      const response = await fetch('http://127.0.0.1:5555/logout', { method: 'DELETE' });

      if (response.ok) {
        // Clear the user context on successful logout
        setUser({ id: null, username: '', email: '', role: '' });
        // Navigate back to the home page or any desired page
        navigate('/');
      } else {
        console.error('Failed to log out');
      }
    } catch (error) {
      console.error('Error logging out:', error);
    }
  };

  return (
    <nav>
      <Link to="/">Home</Link>

      {/* Conditional Rendering Based on User Role */}
      {user.id ? (
        <>
          <Link to="/admin/dashboard">AdminDashboard</Link>

          {user.role === 'user' && <Link to="/inventory">Inventory</Link>}
          {(user.role === 'user' || user.role === 'mover') && (
            <>
              <Link to="/quotes">Quotes</Link>
              <Link to="/moves">Moves</Link>
            </>
          )}
          <button onClick={handleLogout}>Logout</button>
        </>
      ) : (
        <>
          <Link to="/login">Login</Link>
          <Link to="/register">Register</Link>
        </>
      )}
    </nav>
  );
};

export default Navbar;
