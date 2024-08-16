// components/Quote.js
import React, { useState, useEffect, useContext } from 'react';
import { UserContext } from '../context/UserContext';

const Quote = () => {
  const [quotes, setQuotes] = useState([]);
  const [newQuote, setNewQuote] = useState({ move_id: '', price: '', status: '' });
  const { user } = useContext(UserContext);

  useEffect(() => {
    const fetchQuotes = async () => {
      const response = await fetch('http://127.0.0.1:5000/quotes');
      const data = await response.json();
      setQuotes(data);
    };

    fetchQuotes();
  }, []);

  const handleChange = (e) => {
    setNewQuote({ ...newQuote, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('http://127.0.0.1:5000/quotes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newQuote)
    });
    const data = await response.json();
    setQuotes([...quotes, data]);
    setNewQuote({ move_id: '', price: '', status: '' });
  };

  const handleDelete = async (id) => {
    const response = await fetch(`http://127.0.0.1:5000/quotes/${id}`, {
      method: 'DELETE'
    });
    if (response.ok) {
      setQuotes(quotes.filter(quote => quote.id !== id));
    } else {
      console.error('Delete failed');
    }
  };

  return (
    <div>
      <h2>Quotes</h2>
      {(user.role === 'user' || user.role === 'company') && (
        <form onSubmit={handleSubmit}>
          <label>
            Move ID:
            <input type="text" name="move_id" value={newQuote.move_id} onChange={handleChange} required />
          </label>
          <label>
            Price:
            <input type="number" name="price" value={newQuote.price} onChange={handleChange} required />
          </label>
          <label>
            Status:
            <input type="text" name="status" value={newQuote.status} onChange={handleChange} required />
          </label>
          <button type="submit">Add Quote</button>
        </form>
      )}
      <ul>
        {quotes.map(quote => (
          <li key={quote.id}>
            <span>Move ID: {quote.move_id} - Price: {quote.price} - Status: {quote.status}</span>
            {(user.role === 'user' || user.role === 'company') && <button onClick={() => handleDelete(quote.id)}>Delete</button>}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Quote;
// import React from 'react';
// import { useUser } from '../context/UserContext'; // Correct import

// const Quote = () => {
//   const { isAuthenticated } = useUser();

//   if (!isAuthenticated) {
//     return <p>You need to log in to view this page.</p>;
//   }

//   return (
//     <div>
//       <h1>Quote Page</h1>
//       {/* Page content */}
//     </div>
//   );
// };

// export default Quote;
