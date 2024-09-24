import React from 'react';
import './ChatMessage.css';

function ChatMessage({ message }) {
  return (
    <div className="chat-message">
      {/* <strong>{message.user}:</strong> {message.text} */}
      <strong>{message}</strong>
    </div>
  );
}

export default ChatMessage;
