import unittest
from flask import Flask, jsonify
from main import app, ClaimsManager, Policy, Policyholder  # Import your app and classes

class TestClaimsManagementAPI(unittest.TestCase):

    # Set up the Flask test client
    def setUp(self):
        self.app = app.test_client()  # Get the test client from the Flask app
        self.app.testing = True        # Enable testing mode for error handling

    def test_create_claim_success(self):
        # Test case for creating a claim successfully
        data = {
            "claim_id": 1001,
            "policy_id": 101,
            "amount": 5000
        }

        response = self.app.post("/claim", json=data)  # Send a POST request to the /claim endpoint
        self.assertEqual(response.status_code, 200)  # Assert that the response status is 200 (success)
        self.assertIn('message', response.json)      # Assert that 'message' is in the response body

    def test_create_claim_amount_exceeds_coverage(self):
        # Test case where claim amount exceeds policy coverage
        data = {
            "claim_id": 1002,
            "policy_id": 101,
            "amount": 15000  # Exceeds the coverage amount of 10000
        }

        response = self.app.post("/claim", json=data)
        self.assertEqual(response.status_code, 400)  # Expecting a 400 error due to validation failure
        self.assertIn('error', response.json)        # Assert that an error message is returned

    def test_get_claim(self):
        # Test case for getting an existing claim by claim_id
        data = {
            "claim_id": 1001,
            "policy_id": 101,
            "amount": 5000
        }
        self.app.post("/claim", json=data)  # First, create the claim

        # Now, test the GET request to retrieve the claim
        response = self.app.get("/claim/1001")
        self.assertEqual(response.status_code, 200)  # Should return 200 OK
        self.assertIn('claim', response.json)         # The claim should be present in the response

    def test_get_claim_not_found(self):
        # Test case for retrieving a non-existing claim
        response = self.app.get("/claim/9999")  # Claim ID 9999 does not exist
        self.assertEqual(response.status_code, 200)  # Should return 200 OK
        self.assertEqual(response.json['claim'], "Claim not found")  # Assert the response contains the "Claim not found" message


if __name__ == "__main__":
    unittest.main()  # Run the tests when this file is executed
