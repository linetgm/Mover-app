// src/components/AuthTabs.js
import React, { useState } from 'react';
import Login from './Login';
import Register from './Register';
import './AuthTabs.css';

const AuthTabs = () => {
    const [activeTab, setActiveTab] = useState('login');

    const handleTabChange = (tab) => {
        setActiveTab(tab);
    };

    return (
        <div className="auth-tabs-container">
            <div className="tabs">
                <button 
                    className={activeTab === 'login' ? 'active' : ''} 
                    onClick={() => handleTabChange('login')}
                >
                    Login
                </button>
                <button 
                    className={activeTab === 'register' ? 'active' : ''} 
                    onClick={() => handleTabChange('register')}
                >
                    Register
                </button>
            </div>
            <div className="tab-content">
                {activeTab === 'login' && <Login />}
                {activeTab === 'register' && <Register />}
            </div>
        </div>
    );
};

export default AuthTabs;
