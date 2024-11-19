import React, { useState, useEffect } from 'react';
import './dashboard.css';
import { useNavigate } from 'react-router-dom';

function UserViewEventDashboard() {
    const [selectedDiv, setSelectedDiv] = useState('home');
    const [events, setEvents] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchEvents = async () => {
            try {
                const token = localStorage.getItem('token');
                console.log("Token in Page:", token);
                const response = await fetch('http://127.0.0.1:5000/viewevents', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                });

                const data = await response.json();

                if (response.ok) {
                    setEvents(data.events); 
                } else {
                    console.error(data.message || 'Failed to fetch events');
                    alert(data.message || 'Failed to fetch events');
                }
            } catch (error) {
                console.error('Error fetching events:', error);
                alert('An error occurred while fetching events.');
            }
        };

        fetchEvents();
    }, []);

    const handleSignOut = async () => {
        try {
            const token = localStorage.getItem('token'); // Retrieve the token from local storage

            if (!token) {
                console.error('No token found');
                navigate('/login');
                return;
            }

            const response = await fetch('http://127.0.0.1:5000/admin/signout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`, // Include the token in the request
                },
            });

            if (response.ok) {
                console.log('Successfully signed out');
                localStorage.removeItem('token'); // Clear token
                navigate('/');
            } else {
                const errorData = await response.json();
                console.error('Error signing out:', errorData.error || 'Unknown error');
                alert(errorData.error || 'Unknown error');
            }
        } catch (error) {
            console.error('Error during signout:', error);
            alert('An error occurred during signout.');
        }
    };

    const handleDivClick = (divName, navigateTo) => {
        setSelectedDiv(divName);
        navigate(navigateTo);
    };

    const handleEventClick = (eventId) => {
        console.log("ID:", eventId);
        navigate(`/student/eventdetails/${eventId}`); // Pass event ID in the route
    };

    return (
        <div className='dashboard-container'>
            <div className='dashboard-sidebar'>
                <h1 className='app-name'>GatherHub</h1>
                <div
                    className={`dashboard-tab ${selectedDiv === 'home' ? 'selected' : ''}`}
                    onClick={() => handleDivClick('home', '/dashboard')}
                >
                    <span className="material-symbols-outlined">
                        Home
                    </span>
                </div>
                <div
                    className={`dashboard-tab ${selectedDiv === 'signout' ? 'selected' : ''}`}
                    onClick={handleSignOut}
                >
                    <span className="material-symbols-outlined">
                        Signout
                    </span>
                </div>
            </div>
            <div className='dashboard-main'>
                <div className='dashboard-heading'>Welcome to GatherHub</div>
                <div className='events-section'>
                    <h4 className='events-title'>Upcoming Events</h4>
                    {events.length === 0 ? (
                        <div className='no-events'>No events available.</div>
                    ) : (
                        <div className='events-list'>
                            {events.map(([id, title], index) => (
                                <div
                                    key={index}
                                    className='event-card'
                                    onClick={() => handleEventClick(id)} // Navigate with event ID
                                >
                                    <h3>{title}</h3>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default UserViewEventDashboard;
