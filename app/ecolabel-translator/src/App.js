import React, { useState } from 'react';
import './App.css';

function App() {
  const [label, setLabel] = useState('');
  const [results, setResults] = useState(null);
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
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
      const response = await fetch(`${apiURL}/chat/send?m=${input}&t=${token}`, {
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
              {results.ecolabel1 && results.ecolabel1.map((details, index) =>(
                <div onClick={() => handleChatActive(details.eco_label)}>
                  <h3>{details.eco_label}</h3>
                  <img key={index} src={details.image_url} alt="EcoLabel Image" className="eco-label-image"/>
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
