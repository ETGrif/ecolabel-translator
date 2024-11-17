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
  const [token, setToken] = useState(1);
  const apiURL = 'http://127.0.0.1:5000';

  const handleLabelSubmit = async (event) => {
    event.preventDefault();
  
    try {
      const response = await fetch(`${apiURL}/search?q=${label}`, {
        method: 'GET'
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const data = await response.json(); 
      console.log(data);
      setResults((prevResults) => ({
        ...prevResults,
        description: data.eco_labels,
        detailedExplanation: data.descriptions,
        imageUrls: data.image_urls
      })); 
    } catch (error) {
      console.error('Error submitting label:', error);
    }
  };
  

  const handleGetDetailedExplanation = () => {
    console.log(`Requesting detailed explanation for ${label}`);
    setResults((prevResults) => ({
      ...prevResults,
      detailedExplanation: 'Here is a detailed explanation of the eco-label...'
    }));
  };

  const handleMessageSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await fetch(`${apiURL}/chat/send?t=${input}&m=${token}`, {
        method: 'GET'
      });

      if (!response.ok) {
        throw new Error("HTTP error!");
      }

      const data = await response.json();
      console.log(data);
      setMessages([...messages, {sender:'User', text:input}, {sender: 'Assistant', text:data.assistant_message}]);
      setInput('');
    }
    catch (error) {
      console.error('Error submitting user input: ', error);
    }
  };

  const handleEndChat = () => {
    setMessages([]);
    setIsChatActive(false);
    console.log('Chat ended.');
  };

  const handleChatActive = async () => {
    setIsChatActive(true);
    try {
      const response = await fetch(`${apiURL}/chat/init?label=true`, {
        method: 'GET'
      });

      if (!response.ok) {
        throw new Error("HTTP error!");
      }

      const data = await response.json();
      setMessages([...messages, {sender:'Assistant', text:data.assistant_message}]);
      setToken((prevToke) => (prevToke = data.chat_token));
    }
    catch (error) {
      console.error('Error starting chat: ', error);
    }
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
            <div className='ecolabels'>
              {results.description && results.description.map((ecolabel, index) => (
                <p>{ecolabel}</p>
              ))}
            </div>
            <div className='image'>
              {results.imageUrls && results.imageUrls.map((url, index) => (
                <img key={index} src={url} alt={`Image ${index + 1}`} className="eco-label-image" />
              ))}
            </div>
            <div className='description'>
              {results.detailedExplanation && results.detailedExplanation.map((description, index) => (
                <p>{description}</p>
              ))}
            </div>
            <button onClick={() => setResults(null)} className="back-link">Go back</button>
          </div>
        ) : (
          <div>
            {/* Start Chat Button */}
            {!isChatActive && (
              <button onClick={handleChatActive}>Start Chat</button>
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
