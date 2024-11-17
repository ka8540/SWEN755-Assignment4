import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './Login';

import './App.css';
function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/admin" element={<Login />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;