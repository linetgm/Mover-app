import React, { useState } from 'react';


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
        <div style={styles.outerContainer}>
            <div style={styles.container}>
                <h2>Create Profile</h2>
                {error && <p style={styles.error}>{error}</p>}
                <form style={styles.form} onSubmit={handleSubmit}>
                    <label>
                        User id:
                        <input
                            type="text"
                            name="user_id"
                            value={form.user_id}
                            onChange={handleChange}
                            placeholder="user id"
                            required
                            style={styles.input}
                        />
                    </label>
                    <label>
                        First Name:
                        <input
                            type="text"
                            name="first_name"
                            value={form.first_name}
                            onChange={handleChange}
                            placeholder="First Name"
                            required
                            style={styles.input}
                        />
                    </label>
                    <label>
                        Last Name:
                        <input
                            type="text"
                            name="last_name"
                            value={form.last_name}
                            onChange={handleChange}
                            placeholder="Last Name"
                            required
                            style={styles.input}
                        />
                    </label>
                    <label>
                        Phone Number:
                        <input
                            type="text"
                            name="phone_number"
                            value={form.phone_number}
                            onChange={handleChange}
                            placeholder="Phone Number"
                            required
                            style={styles.input}
                        />
                    </label>
                    <label>
                        Preferences:
                        <input
                            type="text"
                            name="preferences"
                            value={form.preferences}
                            onChange={handleChange}
                            placeholder="Preferences"
                            style={styles.input}
                        />
                    </label>
                    <button type="submit" disabled={isSubmitting} style={styles.button}>
                        {isSubmitting ? 'Submitting...' : 'Submit'}
                    </button>
                </form>
            </div>
        </div>
    );
};

// Inline styles
const styles = {
    outerContainer: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        backgroundColor: '#f0f0f0', // Background color of the page
        margin: 0,
    },
    container: {
        maxWidth: '600px',
        width: '100%',
        padding: '20px',
        border: '1px solid #ddd',
        borderRadius: '8px',
        backgroundColor: '#ff6600', // Background color of the form container
        boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)',
    },
    form: {
        display: 'flex',
        flexDirection: 'column',
    },
    input: {
        padding: '8px',
        marginTop: '5px',
        border: '1px solid #ddd',
        borderRadius: '4px',
    },
    button: {
        marginTop: '10px',
        padding: '10px',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
        backgroundColor: '#ff6600',
        color: '#fff',
    },
    buttonDisabled: {
        backgroundColor: '#ccc',
        cursor: 'not-allowed',
    },
    error: {
        color: 'red',
    }
};

export default Profile;
