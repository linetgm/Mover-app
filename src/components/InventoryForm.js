import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const InventoryForm = () => {
  const [houseType, setHouseType] = useState('');
  const [items, setItems] = useState([{ name: '', quantity: 1 }]);
  const [homeTypes, setHomeTypes] = useState([]);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchHomeTypes = async () => {
      try {
        const response = await fetch('http://localhost:5555/home_types');  // Adjust the endpoint as needed
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const types = await response.json();
        setHomeTypes(types);
      } catch (error) {
        console.error('Failed to fetch home types:', error);
        setError('Failed to load home types. Please try again later.');
      }
    };

    fetchHomeTypes();
  }, []);

  const handleItemChange = (index, event) => {
    const { name, value } = event.target;
    setItems(prevItems =>
      prevItems.map((item, i) => (i === index ? { ...item, [name]: value } : item))
    );
  };

  const handleAddItem = () => setItems([...items, { name: '', quantity: 1 }]);

  const handleRemoveItem = (index) => setItems(items.filter((_, i) => i !== index));

  const handleSubmit = async (e) => {
    e.preventDefault();

    const token = localStorage.getItem('access_token');
    console.log('Token retrieved:', token);  // Debugging

    if (!token) {
      setError('No authentication token found. Please log in.');
      return;
    }

    try {
      const inventoryData = {
        house_type: houseType,
        items: items.map(item => ({
          name: item.name.trim(),
          quantity: parseInt(item.quantity, 10) || 1
        }))
      };

      if (inventoryData.items.some(item => !item.name || item.quantity < 1)) {
        setError('Please provide valid item names and quantities.');
        return;
      }

      const response = await fetch('http://localhost:5555/inventory', {  // Adjust the endpoint as needed
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(inventoryData)
      });
      console.log(token)
      if (!response.ok) {
        const errorData = await response.json();
        console.error('Error response:', errorData);  // Debugging
        if (response.status === 401) {
          setError('Unauthorized: Please check your authentication token.');
        } else if (response.status === 400) {
          setError(errorData.msg || 'Bad request');
        } else if (response.status === 500) {
          setError('Internal server error. Please try again later.');
        } else {
          setError(`Error: ${errorData.msg || 'Network response was not ok'}`);
        }
        return;
      }

      alert('Inventory created successfully');
      navigate('/customer');
    } catch (error) {
      console.error('Error creating inventory:', error);
      setError('Failed to create inventory. Please try again later.');
    }
  };

  return (
    <div>
      <h2>Add Inventory</h2>
      {error && <p className="error">{error}</p>}
      <form onSubmit={handleSubmit}>
        <select value={houseType} onChange={(e) => setHouseType(e.target.value)} required>
          <option value="">Select House Type</option>
          {homeTypes.map((type) => (
            <option key={type.id} value={type.type}>{type.type}</option>
          ))}
        </select>

        <div>
          <h3>Items</h3>
          {items.map((item, index) => (
            <div key={index} className="item-form">
              <input
                type="text"
                name="name"
                value={item.name}
                onChange={(event) => handleItemChange(index, event)}
                placeholder="Item Name"
                required
              />
              <input
                type="number"
                name="quantity"
                value={item.quantity}
                onChange={(event) => handleItemChange(index, event)}
                placeholder="Quantity"
                min="1"
                required
              />
              <button type="button" onClick={() => handleRemoveItem(index)}>Remove Item</button>
            </div>
          ))}
          <button type="button" onClick={handleAddItem}>Add Another Item</button>
        </div>

        <button type="submit">Add Inventory</button>
      </form>
    </div>
  );
};

export default InventoryForm;
