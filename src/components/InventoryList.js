import React, { useEffect, useState } from 'react';

const InventoryList = () => {
  const [inventory, setInventory] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchInventory = async () => {
      // Retrieve the token from localStorage
      const token = localStorage.getItem('access_token');

      if (!token) {
        setError('No authentication token found. Please log in.');
        return;
      }

      try {
        const response = await fetch('http://localhost:5555/inventory', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (response.status === 404) {
          const errorData = await response.json();
          setError(errorData.msg || 'No inventory found.');
          setInventory([]); // Ensure inventory is cleared
        } else if (!response.ok) {
          throw new Error('Network response was not ok');
        } else {
          const items = await response.json();
          setInventory(items);
          setError(null); // Clear any previous error
        }
      } catch (error) {
        setError(`Error: ${error.message}`);
      }
    };

    fetchInventory();
  }, []);

  return (
    <div>
      <h2>Your Inventory</h2>
      {error && <p className="error">{error}</p>}
      {inventory.length === 0 && !error ? (
        <p>No inventory found.</p>
      ) : (
        <ul>
          {inventory.map((item) => (
            <li key={item.id}>
              {item.house_type}: {JSON.stringify(item.items)}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default InventoryList;
