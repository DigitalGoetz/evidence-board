import React, { useState, useEffect } from 'react';
import { fetchEvidenceById } from '../services/api';

const EvidenceDetails = ({ evidenceId }) => {
  const [evidence, setEvidence] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await fetchEvidenceById(evidenceId);
        setEvidence(data);
      } catch (err) {
        setError('Failed to fetch evidence details.');
      }
    };

    fetchData();
  }, [evidenceId]);

  if (error) return <p>{error}</p>;
  if (!evidence) return <p>Loading...</p>;

  return (
    <div>
      <h2>Evidence Details</h2>
      <p><strong>Type:</strong> {evidence.evidence.type}</p>
      <p><strong>Description:</strong> {evidence.evidence.description}</p>
      <p><strong>Found At:</strong> {evidence.location.name}</p>
    </div>
  );
};

export default EvidenceDetails;
