from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.user_bucket import validate_user_session, add_event_to_bucket, get_event_audience_type, get_user_major, log_user_activity

class UserAddToBucketAPI(Resource):
    @jwt_required()
    def post(self):
        # Parse the incoming JSON data
        parser = reqparse.RequestParser()
        parser.add_argument('event_id', type=int, required=True, help='Event ID is required', location='json')
        args = parser.parse_args()
        event_id = args['event_id']

        # Get the current user details from JWT
        current_user = get_jwt_identity()
        user_id = current_user.get("id")
        session_key = current_user.get("session_key")
        role = current_user.get("role")

        # # Verify that the role is "Student"
        # if role != "Student":
        #     log_user_activity(session_key, "Unauthorized role attempt to add event", "Failed", user_id)
        #     return make_response(jsonify({"error": "Unauthorized role"}), 403)

        # Validate the user's session
        if not validate_user_session(user_id, session_key):
            log_user_activity(session_key, "Invalid session during add to bucket", "Failed", user_id)
            return make_response(jsonify({"error": "Invalid session or unauthorized access"}), 403)

        # Get the user's major
        user_major = get_user_major(user_id)
        if not user_major:
            log_user_activity(session_key, f"Failed to retrieve user major for user ID {user_id}", "Failed", user_id)
            return make_response(jsonify({"error": "Failed to retrieve user major"}), 500)

        # Get the event's audience type
        audience_type = get_event_audience_type(event_id)
        if not audience_type:
            log_user_activity(session_key, f"Failed to retrieve audience type for event ID {event_id}", "Failed", user_id)
            return make_response(jsonify({"error": "Event not found"}), 404)

        # Check if the user's major matches the event's audience type
        if audience_type != "Both" and user_major != audience_type:
            log_user_activity(session_key, f"Major mismatch for event ID {event_id}", "Denied", user_id)
            return make_response(jsonify({
                "error": f"You must be a {audience_type} student to attend this event."
            }), 310)

        # Add the event to the user's bucket
        try:
            added = add_event_to_bucket(user_id, event_id)
            if not added:
                log_user_activity(session_key, f"Failed to add event ID {event_id} to bucket", "Failed", user_id)
                return make_response(jsonify({"error": "Failed to add event to bucket or already exists"}), 310)
        except Exception as e:
            log_user_activity(session_key, f"Error during add to bucket for event ID {event_id}: {str(e)}", "Error", user_id)
            return make_response(jsonify({"error": f"An error occurred: {str(e)}"}), 500)

        # Log successful action
        log_user_activity(session_key, f"Added event ID {event_id} to bucket", "Success", user_id)

        # Success response
        return make_response(jsonify({"message": "Event added to bucket successfully"}), 201)
