"""Tests for the signup endpoint (POST /activities/{activity_name}/signup)"""

import pytest


class TestSignupEndpoint:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_success(self, client):
        """Test successful signup for a new student"""
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "newstudent@mergington.edu" in data["message"]

    def test_signup_adds_student_to_participants(self, client):
        """Test that signup adds student to activity's participant list"""
        email = "newstudent@mergington.edu"
        
        # Verify student is not in Chess Club initially
        response = client.get("/activities")
        activities = response.json()
        assert email not in activities["Chess Club"]["participants"]
        
        # Sign up
        client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        
        # Verify student is now in Chess Club
        response = client.get("/activities")
        activities = response.json()
        assert email in activities["Chess Club"]["participants"]

    def test_signup_activity_not_found(self, client):
        """Test signup for non-existent activity returns 404"""
        response = client.post(
            "/activities/Nonexistent Activity/signup",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_signup_duplicate_email(self, client):
        """Test signup with email already enrolled returns 400"""
        email = "michael@mergington.edu"  # Already in Chess Club
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]

    def test_signup_missing_email_parameter(self, client):
        """Test signup without email parameter returns 422"""
        response = client.post("/activities/Chess Club/signup")
        assert response.status_code == 422

    def test_signup_multiple_students_same_activity(self, client):
        """Test multiple different students can sign up for same activity"""
        activity = "Programming Class"
        students = ["alice@mergington.edu", "bob@mergington.edu", "charlie@mergington.edu"]
        
        for student in students:
            response = client.post(
                f"/activities/{activity}/signup",
                params={"email": student}
            )
            assert response.status_code == 200
        
        # Verify all students are enrolled
        response = client.get("/activities")
        participants = response.json()[activity]["participants"]
        for student in students:
            assert student in participants

    def test_signup_same_email_different_activities(self, client):
        """Test same student can sign up for multiple different activities"""
        email = "versatile@mergington.edu"
        activities = ["Chess Club", "Programming Class", "Art Club"]
        
        for activity in activities:
            response = client.post(
                f"/activities/{activity}/signup",
                params={"email": email}
            )
            assert response.status_code == 200
        
        # Verify student is in all activities
        response = client.get("/activities")
        all_activities = response.json()
        for activity in activities:
            assert email in all_activities[activity]["participants"]

    @pytest.mark.parametrize("activity_name", [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Tennis Club",
        "Debate Team",
        "Math Olympiad",
        "Art Club",
        "Drama Club"
    ])
    def test_signup_all_activities_exist(self, client, activity_name):
        """Test that signup works for all activity names"""
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": "test@mergington.edu"}
        )
        assert response.status_code == 200
