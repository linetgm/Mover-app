import React from 'react';
import { useNavigate } from 'react-router-dom';

const LogoutButton = ({ logoutEndpoint }) => {
    const navigate = useNavigate();

    const handleLogout = async () => {
        try {
            const response = await fetch(logoutEndpoint, {
                method: 'DELETE',
                credentials: 'include', // This includes cookies with the request
            });

            if (response.ok) {
                // Clear any local storage or session info if necessary
                // Redirect to the login page after logout
                navigate('/login');
            } else {
                console.error('Logout failed');
            }
        } catch (error) {
            console.error('An error occurred during logout:', error);
        }
    };

    return (
        <button onClick={handleLogout}>
            Logout
        </button>
    );
};

export default LogoutButton;
