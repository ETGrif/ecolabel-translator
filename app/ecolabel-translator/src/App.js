import React, { useState } from 'react';
import './App.css';
import leafIcon from './leaf-icon.png';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';


function App() {
  const [label, setLabel] = useState('');
  const [results, setResults] = useState(null);
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [isChatActive, setIsChatActive] = useState(false);
  const [token, setToken] = useState(1);
  const apiURL = 'http://127.0.0.1:5000';
  const popularEcoLabels = [
    {
      "eco_label": "USDA Organic",
      "image_url": "https://www.ecolabelindex.com/files/ecolabel-logos-sized/usda-organic.png",
      "description": 'Commodities, Food'
    },
    {
        "eco_label": "Green Seal",
        "image_url": "https://www.ecolabelindex.com/files/ecolabel-logos-sized/green-seal.png",
        "description": 'Corporate purchasers (excluding retail), Government purchasers'
    },
    {
        "eco_label": "Energy Star USA",
        "image_url": "https://www.ecolabelindex.com/files/ecolabel-logos-sized/energy-star-usa.png",
        "description": 'Forest products / Paper'
    }
  ]


  const handleLabelSubmit = async (event) => {
    event.preventDefault();
  
    try {
      const response = await fetch(`${apiURL}/search?q=${label}`, {
        method: 'GET'
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      let data = await response.json();
      data = data["eco_label_data"];
      console.log(data);
      setResults((prevResults) => ({
        ...prevResults,
        ecolabel1: data
      })); 
    } catch (error) {
      console.error('Error submitting label:', error);
    }
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
    setLabel('');
    console.log('Chat ended.');
  };

  const handleGoBack = () => {
    setResults(null);
    setLabel('');
  }

  const handleChatActive = async (event) => {
    setIsChatActive(true);
    setLabel(event);
    setResults(null);
    try {
      const response = await fetch(`${apiURL}/chat/init?label=${event}`, {
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
        <div className="navbar">
          <div className="logo">
            <img src={leafIcon} alt="Logo"/> 
            <a>EcoLabel Translator</a>
          </div>
          <a href="#">Home</a>
          <a href="#">About</a>
          <a href="#">Content</a>
          <a href="#">Others</a>
        </div>
      <div className="container">
        {/* Render the search header and form only on the search page */}
        {!isChatActive && !results && (
          <>
            <h1>Search for an EcoLabel</h1>
            <form onSubmit={handleLabelSubmit} className="search-container">
              <input 
                type="text"
                placeholder='Enter eco-label name'
                required
                value={label}
                onChange={(e) => setLabel(e.target.value)}         
              />
              <button type="submit">
                <FontAwesomeIcon icon={faSearch} />
              </button>
            </form>
          </>
        )}
  
        {/* Display results if available */}
        {results ? (
          <div className="results">
            <h2>Results for "{label}"</h2>
            <div className='ecolabels'> 
              {results.ecolabel1 && results.ecolabel1.map((details, index) => (
                <div key={index} onClick={() => handleChatActive(details.eco_label)}>
                  <p>{details.eco_label}</p>
                  <img src={details.image_url} alt="EcoLabel Image" className="eco-label-image"/>
                  <p>{details.description}</p>
                </div>
              ))}
            </div>
            <button onClick={handleGoBack} className="back-link">Go back</button>
          </div>
        ) : (
          <div>
            {/* Chat Interface */}
            {isChatActive && (
              <div className='chat-interface'>
                <h2>Eco-Label Chat Assistant</h2>
                <div id="message">
                  {messages.map((message, index) => (
                    <p key={index} ><strong>{message.sender}:</strong> {message.text}</p>
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
  
                <button onClick={handleEndChat} className='end-chat'>End Chat</button>
              </div>
            )}
          </div>
        )}
      </div>
      {/* Display popular ecolabels only on the search page */}
      {!isChatActive && !results && (
        <div className='popular'>
          <h3>Most Popular EcoLabels</h3>
          <div className='eco-labels-grid'>
            {popularEcoLabels.map((details, index) => (
              <div key={index} className='eco-label-card' onClick={() => handleChatActive(details.eco_label)}>
                <h3>{details.eco_label}</h3>
                <img src={details.image_url} alt="EcoLabel Image" className="eco-label-image"/>
                <p>{details.description}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}  

export default App;

