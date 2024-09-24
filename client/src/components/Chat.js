import React, { useState } from 'react';
import './Chat.css';
import logo from '../logo.png';
import profile from '../profile.png';
import { sendMessageToApi } from './api';

function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [diseaseName, setDiseaseName] = useState('');

  const sendMessage = async () => {
    if (input.trim() === '') return;

    const userMessage = { sender: 'user', text: input };
    setMessages([...messages, userMessage]);

    setLoading(true);

    try {
      const data = await sendMessageToApi(input, diseaseName);

      const botMessage = { sender: 'bot', text: data.response };
      setMessages([...messages, userMessage, botMessage]);
      if (data.diseaseName!== '') {
        setDiseaseName(data.diseaseName);
      } else {
        setDiseaseName(diseaseName);
      }
    } catch (error) {
      const errorMessage = { sender: 'bot', text: 'אירעה תקלה בשליחת ההודעה, אנא נסה שוב מאוחר יותר.' };
      setMessages([...messages, userMessage, errorMessage]);
      console.error('Error:', error);
    }

    setLoading(false);
    setInput('');
  };

  return (
    <>
      <div className="logoContainer">
        <img src={logo} alt="Logo" />
        <h1 id='titel_1'>CareBot</h1>
      </div>
      <div className="chatContainer" dir="rtl" lang="he">
        <div className="messagesContainer">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`message ${message.sender === 'user'? 'userMessage' : 'botMessage'}`}
            >
              <img src={message.sender === 'user'? profile : logo} alt="Profile" />
              <div
                dangerouslySetInnerHTML={{
                  __html: message.text.replace(/<script[^>]*>/gi, '').replace(/javascript:/gi, '')
                }}
              />
            </div>
          ))}
          {loading && (
            <div className="loading">
              <div className="spinner"></div>
            </div>
          )}
        </div>
        <div className="inputContainer">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="input"
          />
          <button onClick={sendMessage} className="button">
            שלח
          </button>
        </div>
      </div>
    </>
  );
}

export default Chat;