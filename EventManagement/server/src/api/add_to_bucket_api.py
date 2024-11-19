from datetime import datetime
from flask import jsonify, make_response, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.event_bucket import add_event_to_bucket, is_event_eligible, log_event_activity


class AddToBucketAPI(Resource):
    @jwt_required()
    def post(self):
        # Extract user info from JWT token
        current_user = get_jwt_identity()
        user_id = current_user.get("id")
        major = current_user.get("major")

        # Parse event_id from request body
        data = request.get_json()
        event_id = data.get("event_id")
        if not event_id:
            return make_response(jsonify({"error": "Event ID is required"}), 400)

        # Check eligibility
        eligibility = is_event_eligible(event_id, major)
        if not eligibility["eligible"]:
            log_event_activity(user_id, f"Attempted to add ineligible event ID: {event_id}", "Failed")
            return make_response(jsonify({"error": eligibility["message"]}), 403)

        # Add event to bucket
        success = add_event_to_bucket(user_id, event_id)
        if not success:
            log_event_activity(user_id, f"Failed to add event ID: {event_id} to bucket", "Failed")
            return make_response(jsonify({"error": "Failed to add event to bucket"}), 500)

        # Log successful addition
        log_event_activity(user_id, f"Successfully added event ID: {event_id} to bucket", "Success")
        return make_response(jsonify({"message": "Event added to bucket successfully"}), 200)
