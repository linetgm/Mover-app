// components/Inventory.js
import React, { useState, useEffect, useContext } from 'react';
import { UserContext } from '../context/UserContext';

const Inventory = () => {
  const [inventoryItems, setInventoryItems] = useState([]);
  const [newItem, setNewItem] = useState({ name: '', description: '' });
  const { user } = useContext(UserContext);

  useEffect(() => {
    const fetchInventory = async () => {
      const response = await fetch('http://127.0.0.1:5000/inventories');
      const data = await response.json();
      setInventoryItems(data);
    };

    fetchInventory();
  }, []);

  const handleChange = (e) => {
    setNewItem({ ...newItem, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('http://127.0.0.1:5000/inventories', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newItem)
    });
    const data = await response.json();
    setInventoryItems([...inventoryItems, data]);
    setNewItem({ name: '', description: '' });
  };

  const handleDelete = async (id) => {
    const response = await fetch(`http://127.0.0.1:5000/inventories/${id}`, {
      method: 'DELETE'
    });
    if (response.ok) {
      setInventoryItems(inventoryItems.filter(item => item.id !== id));
    } else {
      console.error('Delete failed');
    }
  };

  return (
    <div>
      <h2>Inventory</h2>
      {user.role === 'admin' && (
        <form onSubmit={handleSubmit}>
          <label>
            Name:
            <input type="text" name="name" value={newItem.name} onChange={handleChange} required />
          </label>
          <label>
            Description:
            <input type="text" name="description" value={newItem.description} onChange={handleChange} />
          </label>
          <button type="submit">Add Item</button>
        </form>
      )}
      <ul>
        {inventoryItems.map(item => (
          <li key={item.id}>
            <span>{item.name} - {item.description}</span>
            {user.role === 'admin' && <button onClick={() => handleDelete(item.id)}>Delete</button>}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Inventory;
