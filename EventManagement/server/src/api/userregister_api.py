from datetime import datetime
from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from flask_bcrypt import Bcrypt
from db.userregister import register_user_in_db, log_user_activity, is_email_registered
import secrets

class UserRegisterAPI(Resource):
    def __init__(self, **kwargs):
        self.bcrypt = kwargs['bcrypt']

    def post(self):
        # Parse request JSON data
        parser = reqparse.RequestParser()
        parser.add_argument('student_email', type=str, required=True, help='Student email is required', location='json')
        parser.add_argument('username', type=str, required=True, help='Username is required', location='json')
        parser.add_argument('password', type=str, required=True, help='Password is required', location='json')
        parser.add_argument('major', type=str, required=True, choices=('UG', 'G'), help='Major must be UG or G', location='json')
        args = parser.parse_args()

        # Check if the email is already registered
        if is_email_registered(args['student_email']):
            return make_response(jsonify({"error": "Email is already registered"}), 400)

        # Hash the password
        hashed_password = self.bcrypt.generate_password_hash(args['password']).decode('utf-8')

        # Generate session key
        session_key = secrets.token_hex(16)
        print('session_key:',session_key)

        # Register the user in the database
        user_data = {
            "student_email": args['student_email'],
            "username": args['username'],
            "password": hashed_password,
            "major": args['major'],
            "role": "Student",
            "session_key": session_key,
        }
        user_id = register_user_in_db(user_data)

        if not user_id:
            return make_response(jsonify({"error": "Failed to register user"}), 500)

        # Log the user activity
        try:
            activity_data = {
                "session_key": session_key,
                "data": f"User {args['username']} registered.",
                "timestamp": datetime.utcnow(),
            }
            log_user_activity(activity_data, user_id)
        except Exception as e:
            return make_response(jsonify({"error": f"User registered, but activity logging failed: {str(e)}"}), 500)

        return make_response(jsonify({"message": "User registered successfully"}), 200)
