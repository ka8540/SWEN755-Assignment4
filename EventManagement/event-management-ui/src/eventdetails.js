import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './adminEventDetails.css'; // Ensure to create a relevant CSS file for this component

function EventDetails() {
    const { eventId } = useParams(); // Get event ID from the URL
    const navigate = useNavigate();
    const [eventDetails, setEventDetails] = useState({});

    useEffect(() => {
        const fetchEventDetails = async () => {
            try {
                const token = localStorage.getItem('token'); // Get the user's token
                console.log("Fetching Event ID:", eventId);

                const response = await fetch(`http://127.0.0.1:5000/eventdetails/${eventId}`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                });

                const data = await response.json();
                console.log("Data:",data);
                if (response.ok) {
                    setEventDetails(data.event_details);
                } else {
                    console.error(data.message || 'Failed to fetch event details');
                }
            } catch (error) {
                console.error('Error fetching event details:', error);
            }
        };

        fetchEventDetails();
    }, [eventId]);

    return (
        <div className="event-details-container">
            {eventDetails && (
                <div className="event-details-card">
                    <h2>Event Details</h2>
                    <div className="event-field">
                        <label>Title:</label>
                        <span>{eventDetails.title}</span>
                    </div>
                    <div className="event-field">
                        <label>Description:</label>
                        <span>{eventDetails.description}</span>
                    </div>
                    <div className="event-field">
                        <label>Date:</label>
                        <span>{eventDetails.date}</span>
                    </div>
                    <div className="event-field">
                        <label>Time:</label>
                        <span>{eventDetails.time}</span>
                    </div>
                    <div className="event-field">
                        <label>Location:</label>
                        <span>{eventDetails.location}</span>
                    </div>
                    <div className="event-field">
                        <label>Organizer:</label>
                        <span>{eventDetails.organizer}</span>
                    </div>
                    <div className="event-field">
                        <label>Audience Type:</label>
                        <span>{eventDetails.audience_type}</span>
                    </div>
                    <div className="event-buttons">
                        <button className="back-btn" onClick={() => navigate('/userdashboard')}>
                            Back to Events
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}

export default EventDetails;
