import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div>
      <h1>Welcome to the Evidence Board</h1>
      <p>Explore and manage evidence for your investigations.</p>
      <nav>
        <ul>
          <li><Link to="/evidence-list">View Evidence List</Link></li>
          <li><Link to="/add-evidence">Add New Evidence (Coming Soon)</Link></li>
        </ul>
      </nav>
    </div>
  );
};

export default Home;
