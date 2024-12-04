import unittest
import requests

class AdminManipulationTestCase(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000" 

    def test_admin_add_user_to_event(self):
        """Test the admin's ability to add a user to an event without validation."""
        # Step 1: Register a new user
        user_payload = {
            "student_email": "testuser@example.com",
            "username": "testuser",
            "password": "password123",
            "major": "UG"
        }
        user_response = requests.post(f"{self.BASE_URL}/register", json=user_payload)

        # Step 2: Log in as the registered user
        login_payload = {
            "username": "testuser",
            "password": "password123"
        }
        login_response = requests.post(f"{self.BASE_URL}/login", json=login_payload)
        
        # Extract the token
        access_token = login_response.json().get("access_token")
        
        import jwt
        decoded_token = jwt.decode(access_token, options={"verify_signature": False})
        user_id = decoded_token.get("sub").get("id")


        # Step 2: Log in as admin
        admin_payload = {
            "username": "admin",
            "password": "admin"
        }
        admin_login_response = requests.post(f"{self.BASE_URL}/admin/login", json=admin_payload)
        admin_token = admin_login_response.json().get("access_token")

        # Step 3: Create a new event as admin
        event_payload = {
            "date": "2024-12-31",
            "description": "Test Event Description",
            "title": "XYZ Event",
            "location": "Test Location",
            "time": "10:00:00",
            "organizer": "Test Organizer",
            "audience_type": "UG"
        }
        event_headers = {"Authorization": f"Bearer {admin_token}"}
        event_response = requests.post(f"{self.BASE_URL}/admin/addevent", json=event_payload, headers=event_headers)

        # Step 4: Fetch all events as admin
        fetch_headers = {"Authorization": f"Bearer {admin_token}"}
        fetch_response = requests.get(f"{self.BASE_URL}/admin/addevent", headers=fetch_headers)

        events = fetch_response.json().get("events")

        # Step 5: Add the user to the event using admin privileges
        add_user_payload = {
            "user_id": user_id,
            "event_id": events[0][0]
        }
        add_user_response = requests.post(f"{self.BASE_URL}/addtobucket", json=add_user_payload, headers=event_headers)

        self.assertEqual(
            add_user_response.status_code,
            403,
            f"Expected 403 but got {add_user_response.status_code}: {add_user_response.json()}"
        )

if __name__ == "__main__":
    unittest.main()
