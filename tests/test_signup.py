"""Tests for the POST /activities/{activity_name}/signup endpoint."""

import pytest


class TestSignup:
    """Test suite for signing up students for activities."""

    def test_signup_new_student_success(self, client):
        """
        Test successful signup of a new student to an activity.
        
        AAA Pattern:
        - ARRANGE: Prepare activity name and new student email
        - ACT: Send POST signup request
        - ASSERT: Verify response status and message
        """
        # ARRANGE: Test data
        activity_name = "Chess Club"
        email = "new.student@mergington.edu"

        # ACT: Sign up student
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # ASSERT: Verify success response
        assert response.status_code == 200
        assert email in response.json()["message"]
        assert activity_name in response.json()["message"]

    def test_signup_adds_participant_to_activity(self, client):
        """
        Test that signup adds the student to the activity's participant list.
        
        AAA Pattern:
        - ARRANGE: Prepare activity name and new student email
        - ACT: Sign up student and fetch activity details
        - ASSERT: Verify participant appears in activity's participant list
        """
        # ARRANGE: Test data
        activity_name = "Programming Class"
        email = "new.student@mergington.edu"

        # ACT: Sign up and fetch updated activities
        client.post(f"/activities/{activity_name}/signup", params={"email": email})
        response = client.get("/activities")
        activities = response.json()

        # ASSERT: Verify student is now in participants
        assert email in activities[activity_name]["participants"]

    def test_signup_decreases_available_spots(self, client):
        """
        Test that signup decreases the number of available spots.
        
        AAA Pattern:
        - ARRANGE: Fetch initial spot availability
        - ACT: Sign up a student
        - ASSERT: Verify available spots decreased by 1
        """
        # ARRANGE: Get initial state
        response = client.get("/activities")
        activities = response.json()
        initial_count = len(activities["Tennis Club"]["participants"])
        max_spots = activities["Tennis Club"]["max_participants"]
        initial_available = max_spots - initial_count

        # ACT: Sign up new student
        email = "new.student@mergington.edu"
        client.post("/activities/Tennis Club/signup", params={"email": email})

        # ASSERT: Verify available spots decreased
        response = client.get("/activities")
        activities = response.json()
        new_count = len(activities["Tennis Club"]["participants"])
        new_available = max_spots - new_count
        assert new_available == initial_available - 1

    def test_signup_same_student_twice_fails(self, client):
        """
        Test that a student cannot sign up twice for the same activity.
        
        AAA Pattern:
        - ARRANGE: Sign up student once
        - ACT: Attempt to sign up the same student again
        - ASSERT: Verify second signup is rejected with 400 error
        """
        # ARRANGE: Sign up first time
        activity_name = "Art Studio"
        email = "new.student@mergington.edu"
        client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # ACT: Attempt second signup
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # ASSERT: Verify error response
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_nonexistent_activity_fails(self, client):
        """
        Test that signup to a non-existent activity returns 404.
        
        AAA Pattern:
        - ARRANGE: Prepare request with invalid activity name
        - ACT: Send POST request to non-existent activity
        - ASSERT: Verify 404 response
        """
        # ARRANGE: Test data with invalid activity
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # ACT: Attempt signup
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # ASSERT: Verify not found error
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_signup_url_encoded_activity_name(self, client):
        """
        Test signup with URL-encoded activity name containing spaces.
        
        AAA Pattern:
        - ARRANGE: Prepare request with URL-encoded activity name
        - ACT: Send signup request
        - ASSERT: Verify successful signup
        """
        # ARRANGE: Activity with spaces in name
        activity_name = "Basketball Team"
        email = "new.student@mergington.edu"

        # ACT: Sign up (requests handles encoding)
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # ASSERT: Verify success
        assert response.status_code == 200
        assert email in response.json()["message"]

    @pytest.mark.parametrize("activity_name", [
        "Chess Club",
        "Programming Class",
        "Gym Class",
    ])
    def test_signup_multiple_activities(self, client, activity_name):
        """
        Test signup functionality across multiple activities.
        
        AAA Pattern:
        - ARRANGE: Parametrize different activity names
        - ACT: Sign up to each activity with unique email
        - ASSERT: Verify successful signup for all activities
        """
        # ARRANGE: Parametrized activity name and test email
        email = f"student.for.{activity_name.replace(' ', '_')}@mergington.edu"

        # ACT: Sign up
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # ASSERT: Verify success
        assert response.status_code == 200

    def test_signup_multiple_students_to_same_activity(self, client):
        """
        Test that multiple different students can sign up for the same activity.
        
        AAA Pattern:
        - ARRANGE: Prepare multiple student emails
        - ACT: Sign up multiple students to the same activity
        - ASSERT: Verify all students are added to participants
        """
        # ARRANGE: Multiple unique students
        activity_name = "Music Band"
        students = [
            "student1@mergington.edu",
            "student2@mergington.edu",
            "student3@mergington.edu"
        ]

        # ACT: Sign up all students
        for email in students:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == 200

        # ASSERT: Verify all students in participants
        response = client.get("/activities")
        participants = response.json()[activity_name]["participants"]
        for email in students:
            assert email in participants

    def test_signup_existing_participant_email_already_registered(self, client):
        """
        Test that an existing registered participant cannot signup again.
        
        AAA Pattern:
        - ARRANGE: Get an email of existing participant
        - ACT: Attempt to sign up with that email
        - ASSERT: Verify 400 error response
        """
        # ARRANGE: Use existing participant from initialized data
        activity_name = "Chess Club"
        existing_email = "michael@mergington.edu"

        # ACT: Attempt signup with existing email
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )

        # ASSERT: Verify error
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
