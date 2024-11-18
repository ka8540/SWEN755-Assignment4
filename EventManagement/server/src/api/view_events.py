from datetime import datetime
from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.eventdetails import get_all_events, log_user_activity

class ViewEventsAPI(Resource):
    @jwt_required()
    def get(self):
        # Get current user details from JWT
        current_user = get_jwt_identity()
        user_id = current_user.get("id")
        session_key = current_user.get("session_key")
        role = current_user.get("role")

        # Log the user's request
        log_user_activity({
            "session_key": session_key,
            "data": f"User {user_id} requested event list",
            "timestamp": datetime.utcnow()
        }, user_id)

        # Fetch all events from the database
        events = get_all_events()

        # Check if no events were found
        if not events:
            log_user_activity({
                "session_key": session_key,
                "data": "No events found",
                "timestamp": datetime.utcnow()
            }, user_id)
            return make_response(jsonify({"error": "No events found"}), 404)

        # Log successful retrieval of events
        log_user_activity({
            "session_key": session_key,
            "data": "Successfully retrieved event list",
            "timestamp": datetime.utcnow()
        }, user_id)

        # Return the list of events
        return make_response(jsonify({"events": events}), 200)