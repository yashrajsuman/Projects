import React, { useState, useRef, useEffect } from 'react';

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSend = async () => {
    if (input.trim()) {
      setMessages([...messages, { text: input, sender: 'user' }]);
      try {
        const response = await fetch('http://localhost:5000/get_response', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message: input }),
        });
        const data = await response.json();
        setMessages(msgs => [...msgs, { text: data.response, sender: 'bot' }]);
      } catch (error) {
        console.error('Error:', error);
        setMessages(msgs => [...msgs, { text: "Sorry, I'm having trouble connecting to my brain right now.", sender: 'bot' }]);
      }
      setInput('');
    }
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      height: '100vh',
      fontFamily: 'Arial, sans-serif',
      background: 'linear-gradient(to bottom right, #FFEBEE, #FFCDD2)'
    }}>
      <header style={{
        display: 'flex',
        alignItems: 'center',
        padding: '1rem',
        background: 'white',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
      }}>
        <div style={{
          width: '48px',
          height: '48px',
          borderRadius: '50%',
          overflow: 'hidden',
          marginRight: '1rem',
          border: '2px solid #D32F2F',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
        }}>
          <img 
            src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/logo-64KZUuAjKoHfzScffNlIijVSUY2Vme.jpg" 
            alt="Atria Bot Logo" 
            style={{ width: '100%', height: '100%', objectFit: 'cover' }}
          />
        </div>
        <h1 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#D32F2F' }}>Atria Bot</h1>
      </header>
      <div style={{
        flexGrow: 1,
        overflowY: 'auto',
        padding: '1rem',
      }}>
        {messages.map((message, index) => (
          <div
            key={index}
            style={{
              display: 'flex',
              justifyContent: message.sender === 'user' ? 'flex-end' : 'flex-start',
              marginBottom: '1rem'
            }}
          >
            <div
              style={{
                maxWidth: '70%',
                padding: '0.5rem 1rem',
                borderRadius: '1rem',
                background: message.sender === 'user' ? '#2196F3' : 'white',
                color: message.sender === 'user' ? 'white' : 'black',
                boxShadow: '0 1px 2px rgba(0,0,0,0.1)'
              }}
            >
              {message.text}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div style={{
        display: 'flex',
        padding: '1rem',
        background: 'white',
        borderTop: '1px solid #FFCDD2'
      }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Type your message..."
          style={{
            flexGrow: 1,
            marginRight: '0.5rem',
            padding: '0.5rem',
            border: '1px solid #FFCDD2',
            borderRadius: '0.25rem',
            outline: 'none'
          }}
        />
        <button
          onClick={handleSend}
          style={{
            padding: '0.5rem 1rem',
            background: '#D32F2F',
            color: 'white',
            border: 'none',
            borderRadius: '0.25rem',
            cursor: 'pointer'
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
}