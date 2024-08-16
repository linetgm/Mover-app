import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { UserContext } from '../context/UserContext';
import { Navbar, Nav, Button } from 'react-bootstrap';

const NavbarComponent = () => {
  const { user, setUser } = useContext(UserContext);
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5555/logout', { method: 'DELETE' });

      if (response.ok) {
        setUser({ id: null, username: '', email: '', role: '' });
        navigate('/');
      } else {
        console.error('Failed to log out');
      }
    } catch (error) {
      console.error('Error logging out:', error);
    }
  };

  return (
    <Navbar bg="dark" variant="dark" expand="lg" sticky="top">
      <Navbar.Brand as={Link} to="/">Home</Navbar.Brand>
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="mr-auto">
          {user.id ? (
            <>
              <Nav.Link as={Link} to="/admin/dashboard">Admin Dashboard</Nav.Link>
              {user.role === 'user' && <Nav.Link as={Link} to="/inventory">Inventory</Nav.Link>}
              {(user.role === 'user' || user.role === 'mover') && (
                <>
                  <Nav.Link as={Link} to="/quotes">Quotes</Nav.Link>
                  <Nav.Link as={Link} to="/moves">Moves</Nav.Link>
                </>
              )}
              <Button variant="danger" onClick={handleLogout}>Logout</Button>
            </>
          ) : (
            <>
              <Nav.Link as={Link} to="/login">Login</Nav.Link>
              <Nav.Link as={Link} to="/register">Register</Nav.Link>
            </>
          )}
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  );
};

export default NavbarComponent;
