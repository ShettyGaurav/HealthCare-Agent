import React, { useState, useRef, useEffect } from 'react';
import { Heart, AlertCircle } from 'lucide-react';
import ChatMessage from './components/ChatMessage';
import ChatInput from './components/ChatInput';
import SystemStatus from './components/SystemStatus';
import HospitalList from './components/HospitalList';
import AnalysisToggle from './components/AnalysisToggle';
import { healthcareApi } from './api/healthcareApi';

function App() {
  const [messages, setMessages] = useState([
    {
      type: 'assistant',
      content: 'Hello! I\'m your Healthcare AI Triage Assistant. Please describe your symptoms and I\'ll help you find the right medical department and hospital.'
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [useCrewAI, setUseCrewAI] = useState(true);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (message) => {
    setError(null);
    setMessages(prev => [...prev, { type: 'user', content: message }]);
    setIsLoading(true);

    try {
      let result;
      if (useCrewAI) {
        result = await healthcareApi.analyzeSymptomsWithCrew(message);
      } else {
        result = await healthcareApi.analyzeSymptoms(message);
      }

      setMessages(prev => [...prev, { type: 'assistant', content: result }]);
    } catch (error) {
      console.error('Analysis failed:', error);
      setError('Failed to analyze symptoms. Please check if the backend server is running.');
      setMessages(prev => [...prev, { 
        type: 'assistant', 
        content: 'Sorry, I encountered an error while analyzing your symptoms. Please try again or check if the backend server is running.' 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleToggleAnalysis = () => {
    setUseCrewAI(!useCrewAI);
  };

  return (
    <div className="app">
      <header className="header">
        <h1>
          <Heart size={28} />
          Healthcare AI Triage Assistant
        </h1>
      </header>

      <div className="main-container">
        <div className="chat-section">
          <div className="chat-header">
            <h2>Medical Symptom Analysis</h2>
            <p>Powered by {useCrewAI ? 'CrewAI Multi-Agent System' : 'Gemini AI'} with RAG Technology</p>
          </div>

          <div className="chat-messages">
            {messages.map((message, index) => (
              <ChatMessage
                key={index}
                message={message.content}
                type={message.type}
              />
            ))}
            {isLoading && (
              <div className="message assistant">
                <div className="message-avatar">
                  <div className="loading-spinner"></div>
                </div>
                <div className="message-content">
                  <div className="message-bubble">
                    <div className="loading">
                      Analyzing your symptoms using {useCrewAI ? 'CrewAI agents' : 'Gemini AI'}...
                    </div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {error && (
            <div className="error-message">
              <AlertCircle size={16} style={{ display: 'inline', marginRight: '8px' }} />
              {error}
            </div>
          )}

          <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
        </div>

        <div className="sidebar">
          <AnalysisToggle useCrewAI={useCrewAI} onToggle={handleToggleAnalysis} />
          <SystemStatus />
          <HospitalList />
        </div>
      </div>
    </div>
  );
}

export default App;