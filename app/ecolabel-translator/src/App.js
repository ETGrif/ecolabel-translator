import React, { useState } from 'react';
import './App.css';

function App() {
  const [label, setLabel] = useState('');
  const [results, setResults] = useState(null);
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([
    { sender: 'Assistant', text: 'Welcome to the chat!' }
  ]);
  const [isChatActive, setIsChatActive] = useState(false);

  const handleLabelSubmit = (event) => {
    event.preventDefault();
    setResults({
      description: 'This is a sample eco-label description.',
      epaRecommendation: 'EPA recommends this label for sustainable products.'
    });
  };

  const handleGetDetailedExplanation = () => {
    console.log(`Requesting detailed explanation for ${label}`);
    setResults((prevResults) => ({
      ...prevResults,
      detailedExplanation: 'Here is a detailed explanation of the eco-label...'
    }));
  };

  const handleMessageSubmit = (event) => {
    event.preventDefault();
    if (input.trim()) {
      setMessages([...messages, { sender: 'User', text: input }]);
      setInput('');
    }
  };

  const handleEndChat = () => {
    setMessages([]);
    setIsChatActive(false);
    console.log('Chat ended.');
  };

  return (
    <div className="App">
      <div className="container">
        <h1>Eco-Label Translator</h1>

        {/* Search form for Eco-Label */}
        {!isChatActive && (
          <form onSubmit={handleLabelSubmit}>
            <input 
              type="text"
              placeholder='Enter eco-label name'
              required
              value={label}
              onChange={(e) => setLabel(e.target.value)}            
            />
            <button type="submit">Search</button>
          </form>
        )}

        {/* Display results if available */}
        {results ? (
          <div className="results">
            <h2>Results for "{label}"</h2>
            <p><strong>Description:</strong> {results.description}</p>
            <p><strong>EPA Recommendation:</strong> {results.epaRecommendation}</p>

            {results.detailedExplanation ? (
              <p><strong>Detailed Explanation:</strong> {results.detailedExplanation}</p>
            ) : (
              <button onClick={handleGetDetailedExplanation}>
                Get Detailed Explanation
              </button>
            )}
            <button onClick={() => setResults(null)} className="back-link">Go back</button>
          </div>
        ) : (
          <div>
            {/* Start Chat Button */}
            {!isChatActive && (
              <button onClick={() => setIsChatActive(true)}>Start Chat</button>
            )}

            {/* Chat Interface */}
            {isChatActive && (
              <div>
                <h2>Eco-Label Chat Assistant</h2>
                <div id="messages">
                  {messages.map((message, index) => (
                    <p key={index}><strong>{message.sender}:</strong> {message.text}</p>
                  ))}
                </div>

                <form onSubmit={handleMessageSubmit}>
                  <input
                    type="text"
                    placeholder="Type your message..."
                    required
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                  />
                  <button type="submit">Send</button>
                </form>

                <button onClick={handleEndChat}>End Chat</button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
