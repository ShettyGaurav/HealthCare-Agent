import React from 'react';
import { Brain, Users } from 'lucide-react';

const AnalysisToggle = ({ useCrewAI, onToggle }) => {
  return (
    <div className="info-card">
      <h3>
        <Brain size={20} />
        Analysis Method
      </h3>
      <div className="toggle-container">
        <div 
          className={`toggle ${useCrewAI ? 'active' : ''}`}
          onClick={onToggle}
        >
          <div className="toggle-slider"></div>
        </div>
        <span className="toggle-label">
          {useCrewAI ? (
            <>
              <Users size={16} style={{ display: 'inline', marginRight: '4px' }} />
              CrewAI Multi-Agent
            </>
          ) : (
            <>
              <Brain size={16} style={{ display: 'inline', marginRight: '4px' }} />
              Standard AI Analysis
            </>
          )}
        </span>
      </div>
      <div className="status-item">
        <span className="status-label">Current Mode</span>
        <span className="status-value">
          {useCrewAI ? 'Multi-Agent System' : 'Single AI Analysis'}
        </span>
      </div>
      <div className="status-item">
        <span className="status-label">Agents</span>
        <span className="status-value">
          {useCrewAI ? '4 Specialized Agents' : '1 General Agent'}
        </span>
      </div>
    </div>
  );
};

export default AnalysisToggle;