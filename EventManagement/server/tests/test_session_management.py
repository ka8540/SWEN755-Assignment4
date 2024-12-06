import unittest
import requests

class TestSessionManagement(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000" 

    def test_session_mismanagement(self):
        """Test for session mismanagement!!"""
        # Step 1: Register a new user
        user_payload = {
            "student_email": "testuser28@example.com",
            "username": "testuser28",
            "password": "password28",
            "major": "UG"
        }
        user_response = requests.post(f"{self.BASE_URL}/register", json=user_payload)

        # Step 2: Log in as the registered user
        login_payload = {
            "username": "testuser28",
            "password": "password28"
        }
        login_response = requests.post(f"{self.BASE_URL}/login", json=login_payload)
        
        # Extract the token
        access_token = login_response.json().get("access_token")
        
        import jwt
        decoded_token = jwt.decode(access_token, options={"verify_signature": False})
        session_key1 = decoded_token.get("sub").get("session_key")

        # Step 3: Log in as the registered user again
        login_payload = {
            "username": "testuser28",
            "password": "password28"
        }
        login_response = requests.post(f"{self.BASE_URL}/login", json=login_payload)
        
        # Extract the token
        access_token = login_response.json().get("access_token")
        
        import jwt
        decoded_token = jwt.decode(access_token, options={"verify_signature": False})
        session_key2 = decoded_token.get("sub").get("session_key")

        #Assert both generated session keys
        self.assertEqual(
            session_key1,
            session_key2, "These two should be equal"
        )

if __name__ == "__main__":
    unittest.main()
