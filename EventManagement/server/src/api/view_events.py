from flask import jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.eventdetails import get_all_events, get_event_details_by_id, log_user_activity
from datetime import datetime


class ViewEventsAPI(Resource):
    @jwt_required()
    def get(self):
        """
        Get all events available to the user.
        """
        # Get user details from JWT
        current_user = get_jwt_identity()
        user_id = current_user.get("id")
        session_key = current_user.get("session_key")

        # Log activity
        log_user_activity({
            "session_key": session_key,
            "data": f"User {user_id} requested all events",
            "timestamp": datetime.utcnow()
        }, user_id)

        # Fetch all events
        events = get_all_events()

        if not events:
            log_user_activity({
                "session_key": session_key,
                "data": "No events found",
                "timestamp": datetime.utcnow()
            }, user_id)
            return make_response(jsonify({"error": "No events found"}), 404)

        log_user_activity({
            "session_key": session_key,
            "data": "Successfully retrieved event list",
            "timestamp": datetime.utcnow()
        }, user_id)

        return make_response(jsonify({"events": events}), 200)


class ViewEventDetailsAPI(Resource):
    @jwt_required()
    def get(self, event_id):
        """
        Get details of a specific event based on event_id.
        """
        # Get user details from JWT
        current_user = get_jwt_identity()
        user_id = current_user.get("id")
        session_key = current_user.get("session_key")

        # Log activity
        log_user_activity({
            "session_key": session_key,
            "data": f"User {user_id} requested details for event ID {event_id}",
            "timestamp": datetime.utcnow()
        }, user_id)

        # Fetch event details
        event_details = get_event_details_by_id(event_id)

        if not event_details:
            log_user_activity({
                "session_key": session_key,
                "data": f"Event ID {event_id} not found",
                "timestamp": datetime.utcnow()
            }, user_id)
            return make_response(jsonify({"error": "Event not found"}), 404)

        log_user_activity({
            "session_key": session_key,
            "data": f"Successfully retrieved details for event ID {event_id}",
            "timestamp": datetime.utcnow()
        }, user_id)

        return make_response(jsonify({"event_details": event_details}), 200)
