"""Tests for the activities endpoint (GET /activities)"""

import pytest


class TestActivitiesEndpoint:
    """Tests for GET /activities endpoint"""

    def test_get_activities_returns_success(self, client):
        """Test that GET /activities returns 200 status code"""
        response = client.get("/activities")
        assert response.status_code == 200

    def test_get_activities_returns_all_activities(self, client):
        """Test that GET /activities returns all 9 activities"""
        response = client.get("/activities")
        activities = response.json()
        assert len(activities) == 9
        expected_activities = {
            "Chess Club", "Programming Class", "Gym Class",
            "Basketball Team", "Tennis Club", "Debate Team",
            "Math Olympiad", "Art Club", "Drama Club"
        }
        assert set(activities.keys()) == expected_activities

    def test_get_activities_structure(self, client):
        """Test that each activity has required fields"""
        response = client.get("/activities")
        activities = response.json()
        
        required_fields = {"description", "schedule", "max_participants", "participants"}
        for activity_name, activity in activities.items():
            assert isinstance(activity, dict), f"{activity_name} should be a dict"
            assert required_fields.issubset(activity.keys()), \
                f"{activity_name} missing required fields: {required_fields - set(activity.keys())}"
            
            # Validate field types
            assert isinstance(activity["description"], str)
            assert isinstance(activity["schedule"], str)
            assert isinstance(activity["max_participants"], int)
            assert isinstance(activity["participants"], list)
            assert all(isinstance(email, str) for email in activity["participants"])

    def test_get_activities_content_is_json(self, client):
        """Test that response Content-Type is application/json"""
        response = client.get("/activities")
        assert "application/json" in response.headers["content-type"]
