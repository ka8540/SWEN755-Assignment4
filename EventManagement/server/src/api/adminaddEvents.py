from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.adminevents import validate_admin_session, add_event_to_db, log_admin_activity, get_event_titles
from datetime import datetime

class AdminAddEventsAPI(Resource):
    @jwt_required()
    def get(self):
        # Get current user details from JWT
        current_user = get_jwt_identity()
        user_id = current_user.get("id")
        session_key = current_user.get("session_key")

        # Validate admin session
        if not validate_admin_session(user_id, session_key):
            log_admin_activity(session_key, "Invalid session or unauthorized attempt to fetch events", "Failed",user_id)
            return make_response(jsonify({"error": "Invalid session or unauthorized access"}), 403)

        # Fetch all event titles and IDs
        events = get_event_titles()

        # Log the fetch activity
        log_admin_activity(session_key, "Fetched all event titles", "Success",user_id)

        return make_response(jsonify({"events": events}), 200)
    
    @jwt_required()
    def post(self):
        # Parse request JSON data
        parser = reqparse.RequestParser()
        parser.add_argument('date', type=str, required=True, help='Date is required (YYYY-MM-DD)', location='json')
        parser.add_argument('description', type=str, required=True, help='Description is required', location='json')
        parser.add_argument('title', type=str, required=True, help='Title is required', location='json')
        parser.add_argument('location', type=str, required=True, help='Location is required', location='json')
        parser.add_argument('time', type=str, required=True, help='Time is required (HH:MM:SS)', location='json')
        parser.add_argument('organizer', type=str, required=True, help='Organizer is required', location='json')
        args = parser.parse_args()

        # Get current user details from JWT
        current_user = get_jwt_identity()
        user_id = current_user.get("id")
        session_key = current_user.get("session_key")

        # Validate admin session
        if not validate_admin_session(user_id, session_key):
            log_admin_activity(session_key, "Invalid session or unauthorized attempt to add event", "Failed",user_id)
            return make_response(jsonify({"error": "Invalid session or unauthorized access"}), 403)

        # Add event to the database
        event_data = {
            "date": args['date'],
            "description": args['description'],
            "title": args['title'],
            "location": args['location'],
            "time": args['time'],
            "organizer": args['organizer']
        }
        add_event_to_db(event_data)

        # Log the event addition activity
        log_admin_activity(session_key, f"Added event: {args['title']}", "Success",user_id)

        return make_response(jsonify({"message": "Event added successfully"}), 200)
