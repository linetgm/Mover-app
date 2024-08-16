// App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { UserProvider } from './context/UserContext';
import Navbar from './components/Navbar';
import Home from './components/Home';
import Login from './components/Login';
import Register from './components/Register';
import AdminDashboard from './components/AdminDashboard';
import MoverDashboard from './components/MoverDashBoard';
import CustomerDashboard from './components/CustomerDashboard';
import AboutUs from './components/AboutUs'; // Import AboutUs
import 'bootstrap/dist/css/bootstrap.min.css'; // Import Bootstrap CSS
import './App.css'; // Import your custom CSS file
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';

const App = () => {
  return (
    <UserProvider>
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/customer/dashboard" element={<CustomerDashboard />} />
          <Route path="/admin" element={<AdminDashboard />} />
          <Route path="/customer/*" element={<CustomerDashboard />} />
          <Route path="/mover/*" element={<MoverDashboard />} />
          <Route path="/aboutus" element={<AboutUs />} /> {/* Add AboutUs Route */}
        </Routes>
      </Router>
    </UserProvider>
  );
};

export default App;
