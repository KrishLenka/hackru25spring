import React, { useState, useEffect } from 'react';
import './App.css';

const RatingCircle = ({ value, label, onClick }) => {
  const [color, setColor] = useState('#4a90e2');

  useEffect(() => {
    if (value <= 33) {
      setColor('#ff4d4d'); // Red for low values
    } else if (value <= 66) {
      setColor('#ffd700'); // Yellow for medium values
    } else {
      setColor('#32cd32'); // Green for high values
    }
  }, [value]);

  return (
    <div className="rating-circle" onClick={onClick}>
      <svg width="120" height="120">
        <circle cx="60" cy="60" r="50" stroke="#ddd" strokeWidth="8" fill="none" />
        <circle
          cx="60"
          cy="60"
          r="50"
          stroke={color}
          strokeWidth="8"
          fill="none"
          strokeDasharray="314"
          strokeDashoffset={314 - (value / 100) * 314}
          strokeLinecap="round"
          style={{ transition: 'stroke-dashoffset 0.5s ease-in-out, stroke 0.5s ease-in-out' }}
        />
        <text x="60" y="65" textAnchor="middle" fontSize="20px" fontWeight="bold">
          {Math.round(value)}%
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
  const [ratings, setRatings] = useState({ accuracy: 0, extremity: 0, subjectivity: 0 });
  const [selectedRating, setSelectedRating] = useState(null);
  const [ratingDetails, setRatingDetails] = useState('');
  const [showPopup, setShowPopup] = useState(false);

  const extractNumericalRating = (analysisText) => {
    const numbers = analysisText.match(/\d+/g);
    return numbers ? Math.min(parseInt(numbers[0], 10) * 10, 100) : 50;
  };

  const processAnalysis = (analysisResults) => {
    let accuracySum = 0;
    let extremitySum = 0;
    let subjectivitySum = 0;
    let count = 0;

    analysisResults.forEach(result => {
      const lines = result.analysis.split('\n');
      lines.forEach(line => {
        if (line.toLowerCase().includes('accuracy')) {
          accuracySum += extractNumericalRating(line);
        } else if (line.toLowerCase().includes('extremity')) {
          extremitySum += extractNumericalRating(line);
        } else if (line.toLowerCase().includes('subjectivity')) {
          subjectivitySum += extractNumericalRating(line);
        }
      });
      count++;
    });

    return {
      accuracy: count ? accuracySum / count : 0,
      extremity: count ? extremitySum / count : 0,
      subjectivity: count ? subjectivitySum / count : 0
    };
  };

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
      const newRatings = processAnalysis(data.phrase_analysis);
      setRatings(newRatings);

      setMessages(prev => [
        ...prev,
        { 
          text: data.phrase_analysis.map(pa => `${pa.phrase}\n${pa.analysis}`).join('\n\n'),
          sender: 'bot' 
        }
      ]);
    } catch (error) {
      setMessages(prev => [
        ...prev,
        { text: 'Error connecting to the server.', sender: 'bot' }
      ]);
    }

    setLoading(false);
    setUserMessage('');
  };

  const handleRatingClick = (rating) => {
    setSelectedRating(rating);
    setShowPopup(true);

    const analysis = messages[messages.length - 1]?.text.split('\n\n').find(text => 
      text.toLowerCase().includes(rating.toLowerCase())
    );
    setRatingDetails(analysis || 'No details available');
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
          {loading && (
            <div className="message bot">
              <div className="message-text">Analyzing...</div>
            </div>
          )}
        </div>
        <div className="input-container">
          <input
            type="text"
            value={userMessage}
            onChange={(e) => setUserMessage(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Enter text to analyze..."
          />
          <button onClick={sendMessage}>Send</button>
        </div>
      </div>
      <div className="ratings-section">
        <RatingCircle value={ratings.accuracy} label="Accuracy" onClick={() => handleRatingClick('accuracy')} />
        <RatingCircle value={ratings.extremity} label="Extremity" onClick={() => handleRatingClick('extremity')} />
        <RatingCircle value={ratings.subjectivity} label="Subjectivity" onClick={() => handleRatingClick('subjectivity')} />
      </div>

      {showPopup && (
        <div className="popup-overlay" onClick={() => setShowPopup(false)}>
          <div className="popup-content" onClick={(e) => e.stopPropagation()}>
            <h3>{selectedRating} Details</h3>
            <p>{ratingDetails}</p>
            <button onClick={() => setShowPopup(false)}>Close</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
