from flask import jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.userevents import validate_user_session, get_all_events, get_event_details_by_id, log_user_activity
from datetime import datetime

class UserViewEventsAPI(Resource):
    @jwt_required()
    def get(self):
        # Get current user details from JWT
        current_user = get_jwt_identity()
        user_id = current_user.get("id")
        session_key = current_user.get("session_key")
        role = current_user.get("role")

        # Verify role is "Student"
        if role != "Student":
            log_user_activity(session_key, "Unauthorized role attempt to view events", "Failed", user_id)
            return make_response(jsonify({"error": "Unauthorized role"}), 403)

        # Validate user session
        if not validate_user_session(user_id, session_key):
            log_user_activity(session_key, "Invalid session during event fetch", "Failed", user_id)
            return make_response(jsonify({"error": "Invalid session or unauthorized access"}), 403)

        # Fetch all event titles and IDs
        events = get_all_events()
        if not events:
            log_user_activity(session_key, "No events found", "Failed", user_id)
            return make_response(jsonify({"error": "No events found"}), 404)

        # Log successful event fetch
        log_user_activity(session_key, "Fetched all events", "Success", user_id)

        # Return the event titles and IDs
        return make_response(jsonify({"events": events}), 200)

class UserViewEventDetailsAPI(Resource):
    @jwt_required()
    def get(self, event_id):
        # Get current user details from JWT
        current_user = get_jwt_identity()
        user_id = current_user.get("id")
        session_key = current_user.get("session_key")
        role = current_user.get("role")

        # Verify role is "Student"
        if role != "Student":
            log_user_activity(session_key, f"Unauthorized role attempt to view event ID {event_id}", "Failed", user_id)
            return make_response(jsonify({"error": "Unauthorized role"}), 403)

        # Validate user session
        if not validate_user_session(user_id, session_key):
            log_user_activity(session_key, f"Invalid session during event details fetch for ID {event_id}", "Failed", user_id)
            return make_response(jsonify({"error": "Invalid session or unauthorized access"}), 403)

        # Fetch event details by event ID
        event_details = get_event_details_by_id(event_id)
        if not event_details:
            log_user_activity(session_key, f"Event ID {event_id} not found", "Failed", user_id)
            return make_response(jsonify({"error": "Event not found"}), 404)

        # Log successful event details fetch
        log_user_activity(session_key, f"Fetched details for event ID {event_id}", "Success", user_id)

        # Return the event details
        return make_response(jsonify({"event_details": event_details}), 200)
