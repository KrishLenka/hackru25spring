import React, { useState } from "react";
import axios from "axios";
import "./App.css";

const App = () => {
  const [userMessage, setUserMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleUserMessageChange = (e) => {
    setUserMessage(e.target.value);
  };

  const sendMessage = async () => {
    if (!userMessage.trim()) return;

    // Add user message to the chat
    setMessages((prevMessages) => [
      ...prevMessages,
      { text: userMessage, sender: "user" },
    ]);
    setLoading(true);
    setUserMessage("");

    try {
      const response = await axios.post(
        "http://localhost:8000/fact-check-text", // Backend API endpoint
        { text: userMessage } // Send the user message as JSON
      );

      // Extract relevant data from the response
      const { summary, phrase_analysis } = response.data;

      // Prepare the message to show in the chat
      let botMessage = summary || "No summary provided.";
      
      // Add phrase analysis if available
      if (phrase_analysis && phrase_analysis.length > 0) {
        const phraseMessages = phrase_analysis
          .map((item) => `${item.phrase}\nAnalysis: ${item.analysis}`)
          .join("\n\n");

        botMessage += `\n\nAnalysis of Phrases:\n${phraseMessages}`;
      }

      // Add the formatted bot message to the chat
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: botMessage, sender: "bot" },
      ]);
    } catch (error) {
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          text: "Sorry, something went wrong with the backend.",
          sender: "bot",
        },
      ]);
    }
    setLoading(false);
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  };

  return (
    <div className="App">
      <div className="chat-box-container">
        <div className="chat-header">Chat with AI</div>

        <div className="messages-container">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.sender}`}>
              <div className="message-text">{message.text}</div>
            </div>
          ))}
          {loading && (
            <div className="message bot">
              <div className="message-text">Typing...</div>
            </div>
          )}
        </div>

        <div className="input-container">
          <input
            type="text"
            value={userMessage}
            onChange={handleUserMessageChange}
            onKeyPress={handleKeyPress}
            placeholder="Type a message"
          />
          <button onClick={sendMessage}>Send</button>
        </div>
      </div>
    </div>
  );
};

export default App;
