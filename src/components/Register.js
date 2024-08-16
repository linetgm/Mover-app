import React, { useState, useContext } from 'react';
import { UserContext } from '../context/UserContext';
import { useNavigate } from 'react-router-dom';
import './Register.css'; // Ensure this is correctly linked

const Register = () => {
  const [formData, setFormData] = useState({ email: '', password: '', role: 'customer' });
  const { setUser } = useContext(UserContext);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://127.0.0.1:5555/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });
      const data = await response.json();
      if (response.ok) {
        setUser(data);
        navigate('/Login');
      } else {
        console.error('Registration failed:', data);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Register</h2>
      <label>
        Email:
        <input type="email" name="email" value={formData.email} onChange={handleChange} required />
      </label>
      <label>
        Password:
        <input type="password" name="password" value={formData.password} onChange={handleChange} required />
      </label>
      <label>
        Role:
        <select name="role" value={formData.role} onChange={handleChange}>
          <option value="customer">Customer</option>
          <option value="mover">Mover</option>
        </select>
      </label>
      <button type="submit">Register</button>
    </form>
  );
};

export default Register;
