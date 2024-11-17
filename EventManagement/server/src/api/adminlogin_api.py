from datetime import timedelta, datetime
from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from flask_bcrypt import Bcrypt
from db.adminlogin import get_admin_credentials, update_admin_session_key, log_admin_activity
import secrets  

class AdminLoginAPI(Resource):
    def __init__(self, **kwargs):
        self.bcrypt = kwargs['bcrypt']

    def post(self):
        # Parse request JSON data
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='Username is required', location='json')
        parser.add_argument('password', type=str, required=True, help='Password is required', location='json')
        args = parser.parse_args()

        # Fetch admin credentials
        user = get_admin_credentials(args['username'])
        if not user:
            return make_response(jsonify({"error": "Invalid username or role not authorized"}), 403)

        user_id, hashed_password, role = user

        # Verify password
        if not self.bcrypt.check_password_hash(hashed_password, args['password']):
            return make_response(jsonify({"error": "Invalid password"}), 401)

        # Generate secure session key and update in the database
        session_key = secrets.token_hex(16)  # Generates a secure random session key
        update_admin_session_key(user_id, session_key)

        activity_data = {
            "session_key": session_key,
            "data": f"{args['username']} logged in.",
            "timestamp": datetime.utcnow(),
        }
        log_admin_activity(activity_data)

        # Generate JWT token
        expires = timedelta(hours=24)
        access_token = create_access_token(
            identity={"id": user_id, "role": role, "session_key": session_key},
            expires_delta=expires
        )

        return make_response(jsonify({
            "access_token": access_token,
        }), 200)
