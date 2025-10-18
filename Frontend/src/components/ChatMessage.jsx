import React from 'react';
import { User, Bot, CheckCircle } from 'lucide-react';

const ChatMessage = ({ message, type }) => {
  return (
    <div className={`message ${type}`}>
      <div className="message-avatar">
        {type === 'user' ? <User size={20} /> : <Bot size={20} />}
      </div>
      <div className="message-content">
        <div className="message-bubble">
          {typeof message === 'string' ? (
            message
          ) : (
            <TriageResult result={message} />
          )}
        </div>
      </div>
    </div>
  );
};

const TriageResult = ({ result }) => {
  return (
    <div className="triage-result">
      <h3>
        <CheckCircle size={20} />
        Medical Triage Analysis
      </h3>
      <div className="result-item">
        <span className="result-label">Condition:</span>
        <span className="result-value">{result.diagnosis}</span>
      </div>
      <div className="result-item">
        <span className="result-label">Department:</span>
        <span className="result-value">{result.department}</span>
      </div>
      <div className="result-item">
        <span className="result-label">Hospital:</span>
        <span className="result-value">{result.hospital}</span>
      </div>
      <div className="result-item">
        <span className="result-label">Reasoning:</span>
        <span className="result-value">{result.reasoning}</span>
      </div>
      {result.workflow && (
        <div className="result-item">
          <span className="result-label">Workflow:</span>
          <span className="result-value">{result.workflow}</span>
        </div>
      )}
      {result.agents_used && (
        <div className="result-item">
          <span className="result-label">Agents Used:</span>
          <span className="result-value">{result.agents_used}</span>
        </div>
      )}
    </div>
  );
};

export default ChatMessage;