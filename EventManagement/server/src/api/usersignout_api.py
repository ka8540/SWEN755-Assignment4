from datetime import datetime
from flask import jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.userlogin import invalidate_user_session_key, log_user_activity

class UserSignoutAPI(Resource):
    @jwt_required()
    def post(self):
        # Get the user identity from the JWT token
        current_user = get_jwt_identity()
        user_id = current_user.get("id")
        session_key = current_user.get("session_key")

        # Invalidate the session key in the database
        if user_id:
            result = invalidate_user_session_key(user_id)
            if result:
                # Log the sign-out activity
                activity_data = {
                    "session_key": session_key,
                    "data": "User signed out.",
                    "timestamp": datetime.utcnow(),
                }
                log_user_activity(activity_data, user_id)

                return make_response(jsonify({"message": "Successfully signed out"}), 200)
            else:
                return make_response(jsonify({"error": "Failed to sign out"}), 500)
        else:
            return make_response(jsonify({"error": "User not authenticated"}), 401)
