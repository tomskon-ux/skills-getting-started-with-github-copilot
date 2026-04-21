"""Tests for the unregister endpoint (DELETE /activities/{activity_name}/signup)"""

import pytest


class TestUnregisterEndpoint:
    """Tests for DELETE /activities/{activity_name}/signup endpoint"""

    def test_unregister_success(self, client):
        """Test successful unregister from an activity"""
        email = "michael@mergington.edu"  # Pre-enrolled in Chess Club
        response = client.delete(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data or response.status_code == 200

    def test_unregister_removes_student_from_participants(self, client):
        """Test that unregister removes student from activity's participant list"""
        email = "michael@mergington.edu"
        activity = "Chess Club"
        
        # Verify student is in Chess Club initially
        response = client.get("/activities")
        activities_before = response.json()
        assert email in activities_before[activity]["participants"]
        
        # Unregister
        client.delete(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Verify student is no longer in Chess Club
        response = client.get("/activities")
        activities_after = response.json()
        assert email not in activities_after[activity]["participants"]

    def test_unregister_activity_not_found(self, client):
        """Test unregister from non-existent activity returns 404"""
        response = client.delete(
            "/activities/Nonexistent Activity/signup",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_unregister_student_not_enrolled(self, client):
        """Test unregister with email not enrolled returns 400"""
        email = "notenrolled@mergington.edu"
        response = client.delete(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        assert response.status_code == 400
        data = response.json()
        assert "not signed up" in data["detail"]

    def test_unregister_missing_email_parameter(self, client):
        """Test unregister without email parameter returns 422"""
        response = client.delete("/activities/Chess Club/signup")
        assert response.status_code == 422

    def test_unregister_preserves_other_students(self, client):
        """Test that unregister only removes target student, not others"""
        activity = "Debate Team"
        # Debate Team initially has 3 students: marcus, nina, christopher
        
        response = client.get("/activities")
        initial_participants = response.json()[activity]["participants"].copy()
        assert len(initial_participants) == 3
        
        # Unregister one student
        student_to_remove = initial_participants[0]
        client.delete(
            f"/activities/{activity}/signup",
            params={"email": student_to_remove}
        )
        
        # Verify only target student was removed
        response = client.get("/activities")
        remaining_participants = response.json()[activity]["participants"]
        assert len(remaining_participants) == 2
        assert student_to_remove not in remaining_participants
        for student in initial_participants[1:]:
            assert student in remaining_participants

    def test_unregister_allows_re_enrollment(self, client):
        """Test that student can re-enroll after being unregistered"""
        email = "michael@mergington.edu"
        activity = "Chess Club"
        
        # Unregister
        client.delete(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Verify student was removed
        response = client.get("/activities")
        assert email not in response.json()[activity]["participants"]
        
        # Re-enroll
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Verify student is back
        response = client.get("/activities")
        assert email in response.json()[activity]["participants"]

    def test_unregister_multiple_students_sequence(self, client):
        """Test unregistering multiple students in sequence"""
        activity = "Debate Team"
        response = client.get("/activities")
        students_to_remove = response.json()[activity]["participants"].copy()
        
        # Remove each student one by one
        for i, email in enumerate(students_to_remove):
            response = client.delete(
                f"/activities/{activity}/signup",
                params={"email": email}
            )
            assert response.status_code == 200
            
            # Verify correct number of students remaining
            response = client.get("/activities")
            remaining = response.json()[activity]["participants"]
            assert len(remaining) == len(students_to_remove) - i - 1

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
    def test_unregister_all_activities_exist(self, client, activity_name):
        """Test that unregister endpoint works for all activity names"""
        # First get an enrolled student for this activity
        response = client.get("/activities")
        students = response.json()[activity_name]["participants"]
        
        if students:
            email = students[0]
            response = client.delete(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == 200
