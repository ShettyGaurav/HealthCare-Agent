import React, { useState, useEffect } from 'react';
import { Hospital, MapPin } from 'lucide-react';
import { healthcareApi } from '../api/healthcareApi';

const HospitalList = () => {
  const [hospitals, setHospitals] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHospitals = async () => {
      try {
        const data = await healthcareApi.getHospitals();
        setHospitals(data.slice(0, 5));
      } catch (error) {
        console.error('Failed to fetch hospitals:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchHospitals();
  }, []);

  if (loading) {
    return (
      <div className="info-card">
        <h3>
          <Hospital size={20} />
          Available Hospitals
        </h3>
        <div className="loading">
          <div className="loading-spinner"></div>
          Loading hospitals...
        </div>
      </div>
    );
  }

  return (
    <div className="info-card">
      <h3>
        <Hospital size={20} />
        Available Hospitals
      </h3>
      {hospitals.map((hospital, index) => (
        <div key={index} className="status-item">
          <div>
            <div className="status-value">{hospital.name}</div>
            <div className="status-label">
              <MapPin size={12} style={{ display: 'inline', marginRight: '4px' }} />
              {hospital.location} • {hospital.department}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default HospitalList;