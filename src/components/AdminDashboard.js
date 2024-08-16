
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';


const AdminDashboard = () => {
  const navigate = useNavigate();
  const [customers, setCustomers] = useState([]);
  const [movers, setMovers] = useState([]);

  useEffect(() => {
    const fetchCustomersAndMovers = async () => {
      try {
        const token = localStorage.getItem('access_token');
        const headers = { Authorization: `Bearer ${token}` };

        const customersResponse = await fetch('http://localhost:5555/customers', { headers });
        if (!customersResponse.ok) throw new Error('Failed to fetch customers');
        const customersData = await customersResponse.json();
        setCustomers(customersData);

        const moversResponse = await fetch('http://localhost:5555/movers', { headers });
        if (!moversResponse.ok) throw new Error('Failed to fetch movers');
        const moversData = await moversResponse.json();
        setMovers(moversData);
      } catch (error) {
        console.error('Error fetching data', error);
        if (error.message === 'Failed to fetch customers' || error.message === 'Failed to fetch movers') {
          navigate('/');
        }
      }
    };

    fetchCustomersAndMovers();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    navigate('/');
  };

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
      console.error('Error approving mover', error);
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
      console.error('Error rejecting mover', error);
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
      console.error('Error deleting mover', error);
    }
  };

  return (
    <div style={styles.dashboardContainer}>
      <header style={styles.header}>
        <h1 style={styles.title}>Admin Dashboard</h1>
        <button onClick={handleLogout} style={styles.logoutButton}>Logout</button>
      </header>
      
      <div style={styles.sectionContainer}>
        <section style={styles.section}>
          <h2 style={styles.sectionTitle}>Customers</h2>
          <ul style={styles.list}>
            {customers.map(customer => (
              <li key={customer.id} style={styles.listItem}>
                <span>{customer.email}</span>
                <span style={styles.status}>Approved: {customer.approved ? 'Yes' : 'No'}</span>
              </li>
            ))}
          </ul>
        </section>

        <section style={styles.section}>
          <h2 style={styles.sectionTitle}>Movers</h2>
          <ul style={styles.list}>
            {movers.map(mover => (
              <li key={mover.id} style={styles.listItem}>
                <span>{mover.email}</span>
                <span style={styles.status}>Approved: {mover.approved ? 'Yes' : 'No'}</span>
                <div style={styles.buttonGroup}>
                  <button onClick={() => approveMover(mover.id)} style={styles.button}>Approve</button>
                  <button onClick={() => rejectMover(mover.id)} style={styles.button}>Reject</button>
                  <button onClick={() => deleteMover(mover.id)} style={{...styles.button, ...styles.deleteButton}}>Delete</button>
                </div>
              </li>
            ))}
          </ul>
        </section>
      </div>
    </div>
  );
};

const styles = {
  dashboardContainer: {
    padding: '20px',
    fontFamily: 'Arial, sans-serif',
    backgroundColor: '#f5f5f5',
    borderRadius: '8px',
    maxWidth: '120000000px',
    margin: '0 auto',
    marginTop: '80px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '20px',
  },
  title: {
    fontSize: '24px',
    color: '#333',
  },
  logoutButton: {
    padding: '10px 20px',
    backgroundColor: '#ff4d4f',
    color: '#fff',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
  },
  sectionContainer: {
    display: 'flex',
    justifyContent: 'space-between',
    gap: '20px',
  },
  section: {
    flex: 1,
    backgroundColor: '#fff',
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
  },
  sectionTitle: {
    fontSize: '20px',
    marginBottom: '15px',
    color: '#333',
  },
  list: {
    listStyleType: 'none',
    padding: 0,
    margin: 0,
  },
  listItem: {
    padding: '10px 0',
    borderBottom: '1px solid #e0e0e0',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  status: {
    fontSize: '14px',
    color: '#777',
  },
  buttonGroup: {
    display: 'flex',
    gap: '10px',
  },
  button: {
    padding: '8px 12px',
    backgroundColor: '#1890ff',
    color: '#fff',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
  },
  deleteButton: {
    backgroundColor: '#ff4d4f',
  },
};

export default AdminDashboard;
