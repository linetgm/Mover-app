import React, { useState, useEffect } from 'react';

const Moves = ({ onMoveCreated }) => {
    const [moves, setMoves] = useState([]);
    const [companies, setCompanies] = useState([]);
    const [newMove, setNewMove] = useState({
        user_id: '',
        company_id: '',
        current_address: '',
        new_address: '',
        moving_date: '',
        special_requirements: ''
    });
    const [quote, setQuote] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
       
        fetch('http://127.0.0.1:5555/moves')
            .then(response => response.json())
            .then(data => setMoves(data))
            .catch(error => console.error('Error fetching moves:', error));
    }, []);

    useEffect(() => {
        
        fetch('http://127.0.0.1:5555/companies')
            .then(response => response.json())
            .then(data => setCompanies(data))
            .catch(error => console.error('Error fetching companies:', error));
    }, []);

    const handleSubmit = () => {
        setLoading(true);
        fetch('http://127.0.0.1:5555/moves', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newMove),
        })
            .then(response => response.json())
            .then(data => {
                setMoves([...moves, data]);
                onMoveCreated(data.id); // Notify parent about the move creation
                return fetch('http://127.0.0.1:5555/quotes', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(newMove),
                });
            })
            .then(response => response.json())
            .then(data => {
                setQuote(data);
                setLoading(false);
            })
            .catch(error => {
                setError(error.toString());
                setLoading(false);
            });
    };

    return (
        <div style={styles.container}>
            <h2 style={styles.header}>Moves</h2>
            <ul style={styles.movesList}>
                {moves.map(move => (
                    <li key={move.id} style={styles.moveItem}>
                        {move.current_address} to {move.new_address}
                    </li>
                ))}
            </ul>
            <div style={styles.formContainer}>
                <h3 style={styles.formHeader}>Add New Move</h3>
                <select
                    value={newMove.company_id}
                    onChange={e => setNewMove({ ...newMove, company_id: e.target.value })}
                    style={styles.select}
                >
                    <option value="">Select Moving Company</option>
                    {companies.map(company => (
                        <option key={company.id} value={company.id}>
                            {company.name}
                        </option>
                    ))}
                </select>
                <input 
                    type="text" 
                    placeholder="Current Address"
                    value={newMove.current_address}
                    onChange={e => setNewMove({ ...newMove, current_address: e.target.value })}
                    style={styles.input}
                />
                <input 
                    type="text" 
                    placeholder="New Address"
                    value={newMove.new_address}
                    onChange={e => setNewMove({ ...newMove, new_address: e.target.value })}
                    style={styles.input}
                />
                <input 
                    type="date" 
                    placeholder="Moving Date"
                    value={newMove.moving_date}
                    onChange={e => setNewMove({ ...newMove, moving_date: e.target.value })}
                    style={styles.input}
                />
                <input 
                    type="text" 
                    placeholder="Special Requirements"
                    value={newMove.special_requirements}
                    onChange={e => setNewMove({ ...newMove, special_requirements: e.target.value })}
                    style={styles.input}
                />
                <button onClick={handleSubmit} disabled={loading} style={styles.button}>
                    {loading ? 'Submitting...' : 'Add Move and Request Quote'}
                </button>
                {loading && <p style={styles.loading}>Loading...</p>}
                {error && <p style={styles.error}>Error: {error}</p>}
                {quote && (
                    <div style={styles.quote}>
                        <h3>Quote Details</h3>
                        <p><strong>Company:</strong> {quote.company_name}</p>
                        <p><strong>Price:</strong> ${quote.price}</p>
                        <p><strong>Estimated Time:</strong> {quote.estimated_time}</p>
                    </div>
                )}
            </div>
        </div>
    );
};

// Inline styles
const styles = {
    container: {
        maxWidth: '800px',
        margin: '0 auto',
        padding: '20px',
        backgroundColor: '#fff',
        borderRadius: '8px',
        boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)',
    },
    header: {
        textAlign: 'center',
        marginBottom: '20px',
    },
    movesList: {
        listStyleType: 'none',
        padding: 0,
    },
    moveItem: {
        padding: '10px',
        borderBottom: '1px solid #ddd',
    },
    formContainer: {
        marginTop: '20px',
    },
    formHeader: {
        marginBottom: '15px',
    },
    select: {
        width: '100%',
        padding: '10px',
        marginBottom: '10px',
        borderRadius: '4px',
        border: '1px solid #ddd',
    },
    input: {
        width: '100%',
        padding: '10px',
        marginBottom: '10px',
        borderRadius: '4px',
        border: '1px solid #ddd',
    },
    button: {
        width: '100%',
        padding: '10px',
        border: 'none',
        borderRadius: '4px',
        backgroundColor: '#ff6600',
        color: '#fff',
        cursor: 'pointer',
        fontSize: '16px',
    },
    loading: {
        textAlign: 'center',
        marginTop: '10px',
    },
    error: {
        color: 'red',
        textAlign: 'center',
    },
    quote: {
        marginTop: '20px',
        padding: '10px',
        border: '1px solid #ddd',
        borderRadius: '4px',
        backgroundColor: '#f9f9f9',
    },
};

export default Moves;