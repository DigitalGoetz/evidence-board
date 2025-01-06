import React from 'react';
import { useParams } from 'react-router-dom';
import EvidenceDetails from '../components/EvidenceDetails';

const EvidencePage = () => {
  const { evidenceId } = useParams();

  return (
    <div>
      <h2>Evidence Details Page</h2>
      <EvidenceDetails evidenceId={evidenceId} />
    </div>
  );
};

export default EvidencePage;
