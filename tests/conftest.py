"""Pytest configuration and shared fixtures for testing the Mergington High School API."""

import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


# Initial activities data for test reset
INITIAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball training and tournaments",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["marcus@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Tennis skills development and friendly matches",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 4:30 PM",
        "max_participants": 16,
        "participants": ["alex@mergington.edu", "jordan@mergington.edu"]
    },
    "Art Studio": {
        "description": "Painting, drawing, and visual arts exploration",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["isabella@mergington.edu"]
    },
    "Music Band": {
        "description": "Learn instruments and perform in school concerts",
        "schedule": "Mondays and Thursdays, 4:00 PM - 5:00 PM",
        "max_participants": 25,
        "participants": ["lucas@mergington.edu", "sarah@mergington.edu"]
    },
    "Debate Club": {
        "description": "Develop argumentation and public speaking skills",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 14,
        "participants": ["noah@mergington.edu"]
    },
    "Science Lab": {
        "description": "Hands-on experiments and STEM exploration",
        "schedule": "Wednesdays and Fridays, 4:00 PM - 5:00 PM",
        "max_participants": 22,
        "participants": ["ava@mergington.edu", "ethan@mergington.edu"]
    }
}


@pytest.fixture
def client():
    """
    Provide a TestClient instance with fresh activities state for each test.
    
    ARRANGE: Reset the global activities dict to initial state before each test
    """
    # Arrange: Clear and reset activities to known initial state
    activities.clear()
    activities.update({name: copy.deepcopy(data) for name, data in INITIAL_ACTIVITIES.items()})
    
    # Yield the test client to the test
    yield TestClient(app)
    
    # Cleanup: Reset activities after test completes
    activities.clear()
    activities.update({name: copy.deepcopy(data) for name, data in INITIAL_ACTIVITIES.items()})


@pytest.fixture
def sample_activities():
    """
    Provide a list of sample activity names and test emails for parametrized tests.
    """
    return {
        "activities": ["Chess Club", "Programming Class", "Gym Class"],
        "sample_email": "test.student@mergington.edu",
        "existing_emails": {
            "Chess Club": ["michael@mergington.edu"],
            "Programming Class": ["emma@mergington.edu"],
            "Gym Class": ["john@mergington.edu"]
        }
    }
