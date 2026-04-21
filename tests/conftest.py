"""Pytest configuration and shared fixtures for API tests"""

import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

# Default state of activities - used to reset between tests
DEFAULT_ACTIVITIES = {
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
        "description": "Competitive basketball league and practice",
        "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu", "james@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Tennis training and tournaments",
        "schedule": "Saturdays, 10:00 AM - 12:00 PM",
        "max_participants": 16,
        "participants": ["sarah@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop argumentation and public speaking skills",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["marcus@mergington.edu", "nina@mergington.edu", "christopher@mergington.edu"]
    },
    "Math Olympiad": {
        "description": "Challenging mathematics competition and problem solving",
        "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
        "max_participants": 14,
        "participants": ["andrew@mergington.edu"]
    },
    "Art Club": {
        "description": "Painting, drawing, and sculpture techniques",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 25,
        "participants": ["isabella@mergington.edu", "mia@mergington.edu"]
    },
    "Drama Club": {
        "description": "Theater performance and acting workshops",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["lucas@mergington.edu", "grace@mergington.edu"]
    }
}


@pytest.fixture
def client():
    """Provides a TestClient for the FastAPI application with reset state."""
    # Reset activities to default state before each test using deep copy
    activities.clear()
    activities.update(copy.deepcopy(DEFAULT_ACTIVITIES))
    
    # Return test client
    return TestClient(app)
