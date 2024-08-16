import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

const Profile = () => {
    const [form, setForm] = useState({
        user_id: '',
        first_name: '',
        last_name: '',
        phone_number: '',
        preferences: ''
    });
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState('');

    // Handle form input change
    const handleChange = (e) => {
        const { name, value } = e.target;
        setForm(prevForm => ({ ...prevForm, [name]: value }));
    };

    // Handle form submission
    const handleSubmit = (e) => {
        e.preventDefault();
        setIsSubmitting(true);

        fetch('http://127.0.0.1:5000/profiles', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(form),
        })
        .then(response => response.json())
        .then(data => {
            // Handle success (e.g., display a success message, clear the form, etc.)
            alert('Profile created successfully!');
            setForm({
                user_id: '',
                first_name: '',
                last_name: '',
                phone_number: '',
                preferences: ''
            });
        })
        .catch(error => {
            setError('Error creating profile');
            console.error('Error:', error);
        })
        .finally(() => setIsSubmitting(false));
    };

    return (
        <div className="d-flex justify-content-center align-items-center vh-100 bg-light">
            <div className="card p-4 shadow-lg" style={{ maxWidth: '600px', width: '100%' }}>
                <h2 className="text-center mb-4">Create Profile</h2>
                {error && <p className="text-danger">{error}</p>}
                <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                        <label htmlFor="user_id" className="form-label">User ID:</label>
                        <input
                            type="text"
                            id="user_id"
                            name="user_id"
                            value={form.user_id}
                            onChange={handleChange}
                            placeholder="User ID"
                            required
                            className="form-control"
                        />
                    </div>
                    <div className="mb-3">
                        <label htmlFor="first_name" className="form-label">First Name:</label>
                        <input
                            type="text"
                            id="first_name"
                            name="first_name"
                            value={form.first_name}
                            onChange={handleChange}
                            placeholder="First Name"
                            required
                            className="form-control"
                        />
                    </div>
                    <div className="mb-3">
                        <label htmlFor="last_name" className="form-label">Last Name:</label>
                        <input
                            type="text"
                            id="last_name"
                            name="last_name"
                            value={form.last_name}
                            onChange={handleChange}
                            placeholder="Last Name"
                            required
                            className="form-control"
                        />
                    </div>
                    <div className="mb-3">
                        <label htmlFor="phone_number" className="form-label">Phone Number:</label>
                        <input
                            type="text"
                            id="phone_number"
                            name="phone_number"
                            value={form.phone_number}
                            onChange={handleChange}
                            placeholder="Phone Number"
                            required
                            className="form-control"
                        />
                    </div>
                    <div className="mb-4">
                        <label htmlFor="preferences" className="form-label">Preferences:</label>
                        <input
                            type="text"
                            id="preferences"
                            name="preferences"
                            value={form.preferences}
                            onChange={handleChange}
                            placeholder="Preferences"
                            className="form-control"
                        />
                    </div>
                    <button 
                        type="submit" 
                        className={`btn btn-primary w-100 ${isSubmitting ? 'disabled' : ''}`}
                    >
                        {isSubmitting ? 'Submitting...' : 'Submit'}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default Profile;
