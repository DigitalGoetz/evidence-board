import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import EvidenceList from './components/EvidenceList';
import EvidencePage from './pages/EvidencePage';

const App = () => {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/evidence-list" element={<EvidenceList />} />
          <Route path="/evidence/:evidenceId" element={<EvidencePage />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
