import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './adminEventDetails.css';

function AdminAddEvent() {
    const navigate = useNavigate();
    const [newEventDetails, setNewEventDetails] = useState({
        title: '',
        description: '',
        date: '',
        time: '',
        location: '',
        organizer: '',
        audience_type: 'Both', // Default value
    });

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setNewEventDetails((prevDetails) => ({
            ...prevDetails,
            [name]: value,
        }));
    };

    const handleSaveEvent = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://127.0.0.1:5000/admin/addevent', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(newEventDetails),
            });

            const data = await response.json();

            if (response.ok) {
                alert('Event added successfully!');
                navigate('/admindashboard');
            } else {
                console.error(data.message || 'Failed to add event');
                alert(data.message || 'Failed to add event');
            }
        } catch (error) {
            console.error('Error adding event:', error);
            alert('An error occurred while adding the event.');
        }
    };

    return (
        <div className="event-details-container">
            <div className="event-details-card">
                <h2>Add New Event</h2>
                <div className="event-field">
                    <label>Title:</label>
                    <input
                        type="text"
                        name="title"
                        value={newEventDetails.title}
                        onChange={handleInputChange}
                        required
                    />
                </div>
                <div className="event-field">
                    <label>Description:</label>
                    <textarea
                        name="description"
                        value={newEventDetails.description}
                        onChange={handleInputChange}
                        required
                    />
                </div>
                <div className="event-field">
                    <label>Date:</label>
                    <input
                        type="date"
                        name="date"
                        value={newEventDetails.date}
                        onChange={handleInputChange}
                        required
                    />
                </div>
                <div className="event-field">
                    <label>Time:</label>
                    <input
                        type="time"
                        name="time"
                        value={newEventDetails.time}
                        onChange={handleInputChange}
                        required
                    />
                </div>
                <div className="event-field">
                    <label>Location:</label>
                    <input
                        type="text"
                        name="location"
                        value={newEventDetails.location}
                        onChange={handleInputChange}
                        required
                    />
                </div>
                <div className="event-field">
                    <label>Organizer:</label>
                    <input
                        type="text"
                        name="organizer"
                        value={newEventDetails.organizer}
                        onChange={handleInputChange}
                        required
                    />
                </div>
                <div className="event-field">
                    <label>Audience Type:</label>
                    <select
                        name="audience_type"
                        value={newEventDetails.audience_type}
                        onChange={handleInputChange}
                        required
                    >
                        <option value="UG">Undergraduate (UG)</option>
                        <option value="G">Graduate (G)</option>
                        <option value="Both">Both</option>
                    </select>
                </div>
                <div className="event-buttons">
                    <button className="save-btn" onClick={handleSaveEvent}>
                        Add Event
                    </button>
                    <button className="back-btn" onClick={() => navigate('/admindashboard')}>
                        Back to Dashboard
                    </button>
                </div>
            </div>
        </div>
    );
}

export default AdminAddEvent;
