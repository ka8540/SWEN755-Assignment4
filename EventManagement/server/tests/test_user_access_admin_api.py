import unittest
import requests

class AdminManipulationTestCase(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000" 

    def test_admin_add_user_to_event(self):
        """Test the admin's ability to add a user to an event without validation."""
        # Step 1: Register a new user
        user_payload = {
            "student_email": "testuser@example.com",
            "username": "testuser2",
            "password": "password123",
            "major": "UG"
        }
        user_response = requests.post(f"{self.BASE_URL}/register", json=user_payload)

        # Step 2: Log in as the registered user
        login_payload = {
            "username": "testuser2",
            "password": "password123"
        }
        login_response = requests.post(f"{self.BASE_URL}/login", json=login_payload)
        
        # Extract the token
        access_token = login_response.json().get("access_token")
        

        fetch_headers = {"Authorization": f"Bearer {access_token}"}
        fetch_response = requests.get(f"{self.BASE_URL}/admin/addevent", headers=fetch_headers)

        self.assertEqual(fetch_response.status_code,403,f"Expected 403:{fetch_response.json()}") 


        

if __name__ == "__main__":
    unittest.main()
