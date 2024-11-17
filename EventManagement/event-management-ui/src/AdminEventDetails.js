import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './adminEventDetails.css';

function AdminEventDetails() {
    const { eventId } = useParams(); // Get event ID from the URL
    const navigate = useNavigate();
    const [eventDetails, setEventDetails] = useState({});
    const [isEditing, setIsEditing] = useState(false);
    const [updatedEventDetails, setUpdatedEventDetails] = useState({});

    useEffect(() => {
        const fetchEventDetails = async () => {
            try {
                const token = localStorage.getItem('token');
                console.log("ID2:",eventId);
                const response = await fetch(`http://127.0.0.1:5000/admin/eventdetails/${eventId}`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                });

                const data = await response.json();

                if (response.ok) {
                    setEventDetails(data.event_details);
                    setUpdatedEventDetails(data.event_details); // Set the initial editable details
                } else {
                    console.error(data.message || 'Failed to fetch event details');
                }
            } catch (error) {
                console.error('Error fetching event details:', error);
            }
        };

        fetchEventDetails();
    }, [eventId]);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setUpdatedEventDetails((prevDetails) => ({
            ...prevDetails,
            [name]: value,
        }));
    };

    const handleSaveChanges = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`http://127.0.0.1:5000/admin/eventdetails/${eventId}`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(updatedEventDetails),
            });

            const data = await response.json();

            if (response.ok) {
                alert('Event updated successfully!');
                setIsEditing(false);
                setEventDetails(updatedEventDetails);
            } else {
                console.error(data.message || 'Failed to update event details');
            }
        } catch (error) {
            console.error('Error updating event details:', error);
        }
    };

    const handleCancel = () => {
        setIsEditing(false);
        setUpdatedEventDetails(eventDetails);
    };

    return (
        <div className="event-details-container">
           
            {eventDetails && (
                <div className="event-details-card">
                     <h2>Event Details</h2>
                    <div className="event-field">
                        <label>Title:</label>
                        {isEditing ? (
                            <input
                                type="text"
                                name="title"
                                value={updatedEventDetails.title || ''}
                                onChange={handleInputChange}
                            />
                        ) : (
                            <span>{eventDetails.title}</span>
                        )}
                    </div>
                    <div className="event-field">
                        <label>Description:</label>
                        {isEditing ? (
                            <textarea
                                name="description"
                                value={updatedEventDetails.description || ''}
                                onChange={handleInputChange}
                            />
                        ) : (
                            <span>{eventDetails.description}</span>
                        )}
                    </div>
                    <div className="event-field">
                        <label>Date:</label>
                        {isEditing ? (
                            <input
                                type="date"
                                name="date"
                                value={updatedEventDetails.date || ''}
                                onChange={handleInputChange}
                            />
                        ) : (
                            <span>{eventDetails.date}</span>
                        )}
                    </div>
                    <div className="event-field">
                        <label>Time:</label>
                        {isEditing ? (
                            <input
                                type="time"
                                name="time"
                                value={updatedEventDetails.time || ''}
                                onChange={handleInputChange}
                            />
                        ) : (
                            <span>{eventDetails.time}</span>
                        )}
                    </div>
                    <div className="event-field">
                        <label>Location:</label>
                        {isEditing ? (
                            <input
                                type="text"
                                name="location"
                                value={updatedEventDetails.location || ''}
                                onChange={handleInputChange}
                            />
                        ) : (
                            <span>{eventDetails.location}</span>
                        )}
                    </div>
                    <div className="event-field">
                        <label>Organizer:</label>
                        {isEditing ? (
                            <input
                                type="text"
                                name="organizer"
                                value={updatedEventDetails.organizer || ''}
                                onChange={handleInputChange}
                            />
                        ) : (
                            <span>{eventDetails.organizer}</span>
                        )}
                    </div>
                    <div className="event-buttons">
                        {isEditing ? (
                            <>
                                <button className="save-btn" onClick={handleSaveChanges}>
                                    Save Changes
                                </button>
                                <button className="cancel-btn" onClick={handleCancel}>
                                    Cancel
                                </button>
                            </>
                        ) : (
                            <button className="edit-btn" onClick={() => setIsEditing(true)}>
                                Edit Event
                            </button>
                        )}
                        <button className="back-btn" onClick={() => navigate('/admindashboard')}>
                            Back to Dashboard
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}

export default AdminEventDetails;
