import React, { useEffect, useState } from 'react';

const MessageView = ({ token, moveId }) => {
  const [messages, setMessages] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMessages = async () => {
      try {
        const response = await fetch(`http://localhost:5000/get_messages/${moveId}`, {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });

        if (!response.ok) throw new Error('Failed to fetch messages');

        const data = await response.json();
        setMessages(data);
      } catch (err) {
        setError(err.message);
      }
    };

    fetchMessages();
  }, [token, moveId]);

  if (error) return <div>{error}</div>;

  return (
    <div>
      <h1>Messages</h1>
      <ul>
        {messages.map((msg) => (
          <li key={msg.timestamp}>
            <p><strong>Sender ID:</strong> {msg.sender_id}</p>
            <p><strong>Content:</strong> {msg.content}</p>
            <p><strong>Timestamp:</strong> {new Date(msg.timestamp).toLocaleString()}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default MessageView;
