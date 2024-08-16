// import React, { useState } from 'react';
// import { sendMessage } from '../api';
// import { getToken } from '../auth';
// import { useNavigate } from 'react-router-dom';

// const SendMessageForm = ({ moveId }) => {
//   const [receiverId, setReceiverId] = useState('');
//   const [content, setContent] = useState('');
//   const navigate = useNavigate();

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     const token = getToken();
//     try {
//       await sendMessage(token, { receiver_id: receiverId, move_id: moveId, content });
//       alert('Message sent successfully');
//       navigate('/customer'); // Redirect or stay on the same page
//     } catch (error) {
//       alert(error.message);
//     }
//   };

//   return (
//     <div>
//       <h2>Send Message</h2>
//       <form onSubmit={handleSubmit}>
//         <input
//           type="number"
//           value={receiverId}
//           onChange={(e) => setReceiverId(e.target.value)}
//           placeholder="Receiver ID"
//           required
//         />
//         <textarea
//           value={content}
//           onChange={(e) => setContent(e.target.value)}
//           placeholder="Message content"
//           required
//         />
//         <button type="submit">Send Message</button>
//       </form>
//     </div>
//   );
// };

// export default SendMessageForm;
// src/components/SendMessage.js
import React, { useState } from 'react';

const SendMessage = ({ token, moveId }) => {
  const [receiverId, setReceiverId] = useState('');
  const [content, setContent] = useState('');
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5555/send_message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          receiver_id: receiverId,
          move_id: moveId,
          content: content,
        }),
      });

      if (!response.ok) throw new Error('Failed to send message');

      setReceiverId('');
      setContent('');
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="number"
        value={receiverId}
        onChange={(e) => setReceiverId(e.target.value)}
        placeholder="Receiver ID"
        required
      />
      <textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="Message Content"
        required
      />
      <button type="submit">Send Message</button>
      {error && <p>{error}</p>}
    </form>
  );
};

export default SendMessage;

