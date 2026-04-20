"""Tests for the DELETE /activities/{activity_name}/participants/{email} endpoint."""

import pytest


class TestUnregister:
    """Test suite for unregistering students from activities."""

    def test_unregister_participant_success(self, client):
        """
        Test successful unregistration of a participant from an activity.
        
        AAA Pattern:
        - ARRANGE: Prepare activity and existing participant email
        - ACT: Send DELETE request to remove participant
        - ASSERT: Verify response status and message
        """
        # ARRANGE: Test data with existing participant
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # ACT: Unregister the participant
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # ASSERT: Verify success response
        assert response.status_code == 200
        assert email in response.json()["message"]
        assert activity_name in response.json()["message"]

    def test_unregister_removes_participant_from_list(self, client):
        """
        Test that unregister removes the participant from the activity's list.
        
        AAA Pattern:
        - ARRANGE: Get initial participant list
        - ACT: Unregister a participant
        - ASSERT: Verify participant no longer in the list
        """
        # ARRANGE: Get initial state
        response = client.get("/activities")
        activities = response.json()
        activity_name = "Programming Class"
        email = "emma@mergington.edu"
        initial_count = len(activities[activity_name]["participants"])

        # ACT: Unregister participant
        client.delete(f"/activities/{activity_name}/participants/{email}")

        # ASSERT: Verify removed
        response = client.get("/activities")
        activities = response.json()
        assert email not in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == initial_count - 1

    def test_unregister_increases_available_spots(self, client):
        """
        Test that unregister increases the number of available spots.
        
        AAA Pattern:
        - ARRANGE: Get initial availability
        - ACT: Unregister a participant
        - ASSERT: Verify available spots increased by 1
        """
        # ARRANGE: Get initial state
        response = client.get("/activities")
        activities = response.json()
        activity_name = "Tennis Club"
        email = "alex@mergington.edu"
        initial_count = len(activities[activity_name]["participants"])
        max_spots = activities[activity_name]["max_participants"]
        initial_available = max_spots - initial_count

        # ACT: Unregister participant
        client.delete(f"/activities/{activity_name}/participants/{email}")

        # ASSERT: Verify spots increased
        response = client.get("/activities")
        activities = response.json()
        new_count = len(activities[activity_name]["participants"])
        new_available = max_spots - new_count
        assert new_available == initial_available + 1

    def test_unregister_nonexistent_participant_fails(self, client):
        """
        Test that unregister of a non-registered participant returns 400.
        
        AAA Pattern:
        - ARRANGE: Prepare request for student not in activity
        - ACT: Send DELETE request
        - ASSERT: Verify 400 error response
        """
        # ARRANGE: Non-existent participant
        activity_name = "Debate Club"
        email = "nonexistent@mergington.edu"

        # ACT: Attempt unregister
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # ASSERT: Verify error
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_unregister_nonexistent_activity_fails(self, client):
        """
        Test that unregister from non-existent activity returns 404.
        
        AAA Pattern:
        - ARRANGE: Prepare request with invalid activity name
        - ACT: Send DELETE request
        - ASSERT: Verify 404 error response
        """
        # ARRANGE: Invalid activity name
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # ACT: Attempt unregister
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # ASSERT: Verify not found error
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_unregister_then_signup_again(self, client):
        """
        Test that a student can re-signup after unregistering.
        
        AAA Pattern:
        - ARRANGE: Get initial setup with participant
        - ACT: Unregister, then sign up again
        - ASSERT: Verify participant is back in the list
        """
        # ARRANGE: Test data
        activity_name = "Gym Class"
        email = "john@mergington.edu"

        # ACT: Unregister
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        assert response.status_code == 200

        # ACT: Sign up again
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # ASSERT: Verify back in participants
        assert response.status_code == 200
        response = client.get("/activities")
        activities = response.json()
        assert email in activities[activity_name]["participants"]

    @pytest.mark.parametrize("activity_name,email", [
        ("Chess Club", "michael@mergington.edu"),
        ("Programming Class", "emma@mergington.edu"),
        ("Basketball Team", "marcus@mergington.edu"),
    ])
    def test_unregister_initial_participants(self, client, activity_name, email):
        """
        Test unregistering initial participants from various activities.
        
        AAA Pattern:
        - ARRANGE: Parametrize activity-email pairs
        - ACT: Unregister respective participants
        - ASSERT: Verify unregister successful
        """
        # ARRANGE: Parametrized activity and email

        # ACT: Unregister
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # ASSERT: Verify success
        assert response.status_code == 200

    def test_unregister_url_encoded_activity_name(self, client):
        """
        Test unregister with URL-encoded activity name.
        
        AAA Pattern:
        - ARRANGE: Prepare activity with spaces and participant email
        - ACT: Send DELETE request
        - ASSERT: Verify successful unregister
        """
        # ARRANGE: Activity with spaces
        activity_name = "Basketball Team"
        email = "marcus@mergington.edu"

        # ACT: Unregister (requests handles encoding)
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # ASSERT: Verify success
        assert response.status_code == 200

    def test_unregister_multiple_participants_independently(self, client):
        """
        Test that unregistering one participant doesn't affect others.
        
        AAA Pattern:
        - ARRANGE: Get activity with multiple participants
        - ACT: Unregister one specific participant
        - ASSERT: Verify only that participant removed, others remain
        """
        # ARRANGE: Activity with multiple participants
        activity_name = "Chess Club"
        participant_to_remove = "michael@mergington.edu"
        participant_to_keep = "daniel@mergington.edu"

        # ACT: Unregister one of them
        response = client.delete(
            f"/activities/{activity_name}/participants/{participant_to_remove}"
        )

        # ASSERT: Verify specific removal
        assert response.status_code == 200
        response = client.get("/activities")
        activities = response.json()
        participants = activities[activity_name]["participants"]
        assert participant_to_remove not in participants
        assert participant_to_keep in participants

    def test_unregister_empty_activity_still_works(self, client):
        """
        Test unregister works correctly even when activity becomes empty.
        
        AAA Pattern:
        - ARRANGE: Remove all participants from a single-participant activity
        - ACT: Unregister the last remaining participant
        - ASSERT: Verify empty participant list
        """
        # ARRANGE: Activity with single participant
        activity_name = "Basketball Team"
        email = "marcus@mergington.edu"

        # ACT: Unregister the only participant
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # ASSERT: Verify activity is now empty
        assert response.status_code == 200
        response = client.get("/activities")
        activities = response.json()
        assert activities[activity_name]["participants"] == []
