from flask import jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.userevents import validate_user_session, get_all_events, get_event_details_by_id
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
            return make_response(jsonify({"error": "Unauthorized role"}), 403)

        # Validate user session
        if not validate_user_session(user_id, session_key):
            return make_response(jsonify({"error": "Invalid session or unauthorized access"}), 403)

        # Fetch all event titles and IDs
        events = get_all_events()
        if not events:
            return make_response(jsonify({"error": "No events found"}), 404)

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
            return make_response(jsonify({"error": "Unauthorized role"}), 403)

        # Validate user session
        if not validate_user_session(user_id, session_key):
            return make_response(jsonify({"error": "Invalid session or unauthorized access"}), 403)

        # Fetch event details by event ID
        event_details = get_event_details_by_id(event_id)
        if not event_details:
            return make_response(jsonify({"error": "Event not found"}), 404)

        # Return the event details
        return make_response(jsonify({"event_details": event_details}), 200)