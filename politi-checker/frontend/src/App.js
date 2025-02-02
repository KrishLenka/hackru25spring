import React, { useState } from 'react';
import './App.css';

const RatingCircle = ({ value, label, onClick }) => {
  return (
    <div className="rating-circle" onClick={onClick}>
      <svg width="120" height="120">
        <circle cx="60" cy="60" r="50" stroke="#ddd" strokeWidth="8" fill="none" />
        <circle
          cx="60"
          cy="60"
          r="50"
          stroke={value <= 3 ? "#ff4d4d" : value <= 6 ? "#ffd700" : "#32cd32"}
          strokeWidth="8"
          fill="none"
          strokeDasharray="314"
          strokeDashoffset={314 - (value / 10) * 314}
          strokeLinecap="round"
          style={{ transition: 'stroke-dashoffset 0.5s ease-in-out' }}
        />
        <text x="60" y="65" textAnchor="middle" fontSize="20px" fontWeight="bold">
          {value}/10
        </text>
      </svg>
      <div className="circle-label">{label}</div>
    </div>
  );
};

const App = () => {
  const [userMessage, setUserMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [ratings, setRatings] = useState({ accuracy: 5, extremity: 5, subjectivity: 5 });
  const [analysis, setAnalysis] = useState({ overall: "", accuracy: "", extremity: "", subjectivity: "" });
  const [showPopup, setShowPopup] = useState(false);
  const [popupText, setPopupText] = useState("");

  const sendMessage = async () => {
    if (!userMessage.trim()) return;

    setMessages(prev => [...prev, { text: userMessage, sender: 'user' }]);
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/fact-check-text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: userMessage })
      });

      const data = await response.json();

      setRatings({
        accuracy: parseInt(data.phrase_analysis[0].accuracy.match(/\d+/)[0]),  
        extremity: parseInt(data.phrase_analysis[0].extremity.match(/\d+/)[0]),  
        subjectivity: parseInt(data.phrase_analysis[0].subjectivity.match(/\d+/)[0])
      });

      setAnalysis({
        overall: data.phrase_analysis[0].overall_analysis,
        accuracy: `Accuracy Analysis: ${data.phrase_analysis[0].accuracy}`,
        extremity: `Extremity Analysis: ${data.phrase_analysis[0].extremity}`,
        subjectivity: `Subjectivity Analysis: ${data.phrase_analysis[0].subjectivity}`
      });

      setMessages(prev => [...prev, { text: data.phrase_analysis[0].overall_analysis, sender: 'bot' }]);
    } catch (error) {
      setMessages(prev => [...prev, { text: 'Error connecting to the server.', sender: 'bot' }]);
    }

    setLoading(false);
    setUserMessage('');
  };

  return (
    <div className="app-container">
      <div className="chat-section">
        <div className="messages-container">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.sender}`}>
              <div className="message-text">{message.text}</div>
            </div>
          ))}
          {loading && <div className="message bot"><div className="message-text">Analyzing...</div></div>}
        </div>
        <div className="input-container">
          <input type="text" value={userMessage} onChange={(e) => setUserMessage(e.target.value)} placeholder="Enter text to analyze..." />
          <button onClick={sendMessage}>Send</button>
        </div>
      </div>
      <div className="ratings-section">
        <RatingCircle value={ratings.accuracy} label="Accuracy" onClick={() => { setPopupText(analysis.accuracy); setShowPopup(true); }} />
        <RatingCircle value={ratings.extremity} label="Extremity" onClick={() => { setPopupText(analysis.extremity); setShowPopup(true); }} />
        <RatingCircle value={ratings.subjectivity} label="Subjectivity" onClick={() => { setPopupText(analysis.subjectivity); setShowPopup(true); }} />
      </div>

      {showPopup && (
        <div className="popup-overlay" onClick={() => setShowPopup(false)}>
          <div className="popup-content">
            <p>{popupText}</p>
            <button onClick={() => setShowPopup(false)}>Close</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
