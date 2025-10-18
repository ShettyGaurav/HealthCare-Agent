import React, { useState, useEffect } from 'react';
import { Activity, AlertCircle } from 'lucide-react';
import { healthcareApi } from '../api/healthcareApi';

const SystemStatus = () => {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const data = await healthcareApi.getHealthStatus();
        setStatus(data);
        setError(null);
      } catch (error) {
        console.error('Failed to fetch system status:', error);
        setError('Backend unavailable');
      } finally {
        setLoading(false);
      }
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="info-card">
        <h3>
          <Activity size={20} />
          System Status
        </h3>
        <div className="loading">
          <div className="loading-spinner"></div>
          Loading status...
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="info-card">
        <h3>
          <AlertCircle size={20} />
          System Status
        </h3>
        <div className="status-item">
          <span className="status-label">Backend</span>
          <span className="status-value" style={{color: '#e53e3e'}}>Offline</span>
        </div>
        <div className="status-item">
          <span className="status-label">Error</span>
          <span className="status-value" style={{color: '#e53e3e', fontSize: '0.8rem'}}>{error}</span>
        </div>
      </div>
    );
  }

  return (
    <div className="info-card">
      <h3>
        <Activity size={20} />
        System Status
      </h3>
      <div className="status-item">
        <span className="status-label">Backend</span>
        <span className="status-badge">{status?.status || 'Unknown'}</span>
      </div>
      <div className="status-item">
        <span className="status-label">Hospitals</span>
        <span className="status-value">{status?.hospitals_loaded || 0}</span>
      </div>
      <div className="status-item">
        <span className="status-label">Knowledge</span>
        <span className="status-value">{status?.knowledge_entries || 0} entries</span>
      </div>
      <div className="status-item">
        <span className="status-label">Vector Index</span>
        <span className="status-value" style={{color: status?.vector_index_loaded ? '#48bb78' : '#e53e3e'}}>
          {status?.vector_index_loaded ? 'Ready' : 'Not Ready'}
        </span>
      </div>
      <div className="status-item">
        <span className="status-label">Vector Docs</span>
        <span className="status-value">{status?.vector_documents || 0}</span>
      </div>
      <div className="status-item">
        <span className="status-label">AI Agents</span>
        <span className="status-value">{status?.crew_agents || 0}</span>
      </div>
      <div className="status-item">
        <span className="status-label">Workflow</span>
        <span className="status-value" style={{fontSize: '0.8rem'}}>{status?.workflow_type || 'Unknown'}</span>
      </div>
    </div>
  );
};

export default SystemStatus;