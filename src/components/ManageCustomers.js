// src/components/ManageCustomers.js
import React, { useEffect, useState } from 'react';

const ManageCustomers = () => {
  const [customers, setCustomers] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCustomers = async () => {
      try {
        const token = localStorage.getItem('access_token');
        const headers = {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        };

        const response = await fetch('http://localhost:5555/customers', { headers });
        if (!response.ok) throw new Error('Failed to fetch customers');
        const data = await response.json();
        setCustomers(data);
      } catch (error) {
        console.error('Error fetching customers:', error);
        setError(error.message);
      }
    };

    fetchCustomers();
  }, []);

  return (
    <div>
      <h2>Customers</h2>
      {error && <p>Error: {error}</p>}
      <ul>
        {customers.length === 0 ? <p>No customers found.</p> : customers.map(customer => (
          <li key={customer.id}>{customer.email} (Approved: {customer.approved ? 'Yes' : 'No'})</li>
        ))}
      </ul>
    </div>
  );
};

export default ManageCustomers;
