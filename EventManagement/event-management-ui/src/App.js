import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './Login';
import Dashboard from './dashboard';
import UserLogin from './UserLogin';
import AdminEventDetails from './AdminEventDetails';
import AdminAddEvent from './AdminAddEvent';
import UserDashboard from "./userdashboard";
import EventDetails from "./eventdetails";
import './App.css';
function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
        <Route path="/" element={<UserLogin />} />
          <Route path="/admin" element={<Login />} />
          <Route path="/admindashboard" element={<Dashboard/>} />
          <Route path="/admin/addeventboard/:eventId" element={<AdminEventDetails />} />
          <Route path="/create-event" element={<AdminAddEvent />} />
          <Route path="/userdashboard" element={<UserDashboard />} />
          <Route path="/eventdetails/:id" element={<EventDetails />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;