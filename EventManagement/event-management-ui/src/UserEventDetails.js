import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './adminEventDetails.css';

function UserEventDetails() {
    const { eventId } = useParams();
    const navigate = useNavigate();
    const [eventDetails, setEventDetails] = useState({});
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        const fetchEventDetails = async () => {
            try {
                const token = localStorage.getItem('token');
                console.log("ID:", eventId);
                const response = await fetch(`http://127.0.0.1:5000/vieweventdetails/${eventId}`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                });

                const data = await response.json();

                if (response.ok) {
                    setEventDetails(data.event_details);
                } else {
                    console.error(data.message || 'Failed to fetch event details');
                    alert(data.message || 'Failed to fetch event details');
                }
            } catch (error) {
                console.error('Error fetching event details:', error);
                alert('An error occurred while fetching event details.');
            }
        };

        fetchEventDetails();
    }, [eventId]);

    const handleAddToBucket = async () => {
        try {
            setIsLoading(true);
            const token = localStorage.getItem('token');
            const response = await fetch('http://127.0.0.1:5000/addtobucket', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ event_id: eventId }),
            });

            const data = await response.json();

            if (response.ok) {
                alert('Event added to your bucket successfully!');
            } else {
                console.error(data.message || 'Failed to add event to bucket');
                alert(data.message || 'Failed to add event to bucket');
            }
        } catch (error) {
            console.error('Error adding event to bucket:', error);
            alert('An error occurred while adding the event to your bucket.');
        } finally {
            setIsLoading(false);
        }
    };

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
                        <button 
                            className="save-btn" 
                            onClick={handleAddToBucket} 
                            disabled={isLoading}
                        >
                            {isLoading ? 'Adding...' : 'Add to Bucket'}
                        </button>
                        <button className="back-btn" onClick={() => navigate('/userdashboard')}>
                            Back to Dashboard
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}

export default UserEventDetails;
