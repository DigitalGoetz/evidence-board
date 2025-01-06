import React, { useState, useEffect } from 'react';
import axios from 'axios';

const EvidenceList = () => {
  const [evidenceList, setEvidenceList] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchEvidenceList = async () => {
      try {
        const response = await axios.get('http://localhost:8000/evidence'); // Adjust endpoint to match backend
        setEvidenceList(response.data);
      } catch (err) {
        setError('Failed to fetch evidence list.');
      }
    };

    fetchEvidenceList();
  }, []);

  if (error) return <p>{error}</p>;
  if (!evidenceList.length) return <p>Loading...</p>;

  return (
    <div>
      <h2>Evidence List</h2>
      <ul>
        {evidenceList.map((evidence) => (
          <li key={evidence.id}>
            <strong>Type:</strong> {evidence.type} - <strong>Description:</strong> {evidence.description}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default EvidenceList;
