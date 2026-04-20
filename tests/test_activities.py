"""Tests for the GET /activities endpoint."""

import pytest


class TestGetActivities:
    """Test suite for retrieving all activities."""

    def test_get_activities_returns_all_activities(self, client):
        """
        Test that GET /activities returns all activities.
        
        AAA Pattern:
        - ARRANGE: Use fixture with initialized activities
        - ACT: Send GET request to /activities
        - ASSERT: Verify response status and all activities are present
        """
        # ARRANGE: Client fixture provides initialized activities

        # ACT: Fetch all activities
        response = client.get("/activities")

        # ASSERT: Verify status and response
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == 9
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Gym Class" in activities
        assert "Basketball Team" in activities
        assert "Tennis Club" in activities
        assert "Art Studio" in activities
        assert "Music Band" in activities
        assert "Debate Club" in activities
        assert "Science Lab" in activities

    def test_activities_have_required_fields(self, client):
        """
        Test that each activity has all required fields.
        
        AAA Pattern:
        - ARRANGE: Use fixture with initialized activities
        - ACT: Fetch activities and examine structure
        - ASSERT: Verify each activity has description, schedule, max_participants, participants
        """
        # ARRANGE: Client fixture provides initialized activities

        # ACT: Fetch activities
        response = client.get("/activities")
        activities = response.json()

        # ASSERT: Verify all required fields present in each activity
        required_fields = {"description", "schedule", "max_participants", "participants"}
        for activity_name, activity_data in activities.items():
            assert set(activity_data.keys()) == required_fields, \
                f"{activity_name} missing required fields"

    def test_activities_have_correct_initial_participants(self, client):
        """
        Test that activities contain the correct initial participants.
        
        AAA Pattern:
        - ARRANGE: Use fixture with initialized activities
        - ACT: Fetch activities and extract participant data
        - ASSERT: Verify initial participant emails match setup
        """
        # ARRANGE: Client fixture provides initialized activities

        # ACT: Fetch activities
        response = client.get("/activities")
        activities = response.json()

        # ASSERT: Verify initial participants for known activities
        assert activities["Chess Club"]["participants"] == [
            "michael@mergington.edu",
            "daniel@mergington.edu"
        ]
        assert activities["Programming Class"]["participants"] == [
            "emma@mergington.edu",
            "sophia@mergington.edu"
        ]
        assert activities["Gym Class"]["participants"] == [
            "john@mergington.edu",
            "olivia@mergington.edu"
        ]
        assert activities["Basketball Team"]["participants"] == [
            "marcus@mergington.edu"
        ]

    def test_activity_max_participants_is_positive_integer(self, client):
        """
        Test that max_participants is a positive integer for all activities.
        
        AAA Pattern:
        - ARRANGE: Use fixture with initialized activities
        - ACT: Fetch activities
        - ASSERT: Verify max_participants is valid for each activity
        """
        # ARRANGE: Client fixture provides initialized activities

        # ACT: Fetch activities
        response = client.get("/activities")
        activities = response.json()

        # ASSERT: Verify max_participants validity
        for activity_name, activity_data in activities.items():
            max_participants = activity_data["max_participants"]
            assert isinstance(max_participants, int), \
                f"{activity_name} max_participants is not an integer"
            assert max_participants > 0, \
                f"{activity_name} max_participants must be positive"

    def test_participants_list_does_not_exceed_max_limit(self, client):
        """
        Test that number of participants never exceeds max_participants.
        
        AAA Pattern:
        - ARRANGE: Use fixture with initialized activities
        - ACT: Fetch activities and count participants
        - ASSERT: Verify participant count <= max_participants
        """
        # ARRANGE: Client fixture provides initialized activities

        # ACT: Fetch activities
        response = client.get("/activities")
        activities = response.json()

        # ASSERT: Verify participant counts don't exceed limits
        for activity_name, activity_data in activities.items():
            participant_count = len(activity_data["participants"])
            max_participants = activity_data["max_participants"]
            assert participant_count <= max_participants, \
                f"{activity_name} has {participant_count} participants but max is {max_participants}"

    @pytest.mark.parametrize("activity_name,min_participants", [
        ("Chess Club", 2),
        ("Programming Class", 2),
        ("Gym Class", 2),
        ("Basketball Team", 1),
    ])
    def test_specific_activities_have_participants(self, client, activity_name, min_participants):
        """
        Test that specific activities have the expected number of participants.
        
        AAA Pattern:
        - ARRANGE: Use fixture and parametrize activity names
        - ACT: Fetch activities and extract participant list
        - ASSERT: Verify participant count meets minimum
        """
        # ARRANGE: Client fixture and parametrized inputs

        # ACT: Fetch and find the activity
        response = client.get("/activities")
        activities = response.json()
        activity = activities[activity_name]

        # ASSERT: Verify participant count
        assert len(activity["participants"]) >= min_participants, \
            f"{activity_name} expected at least {min_participants} participants"
