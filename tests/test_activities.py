"""Tests for activities endpoint using AAA (Arrange-Act-Assert) pattern"""


def test_get_all_activities(client):
    """Test retrieving all activities - AAA Pattern
    
    Arrange: client is ready (from fixture)
    Act: Make GET request
    Assert: Verify response contains all activities
    """
    # Arrange: client fixture provides clean test state

    # Act: Make GET request
    response = client.get("/activities")

    # Assert: Verify response
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_activity_contains_required_fields(client):
    """Test that each activity has required fields - AAA Pattern
    
    Arrange: client fixture provides activities
    Act: Fetch activities and extract one
    Assert: Verify required fields exist
    """
    # Arrange: client fixture provides clean test state

    # Act: Fetch activities
    response = client.get("/activities")
    data = response.json()
    activity = data["Chess Club"]

    # Assert: Check required fields exist
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    assert isinstance(activity["participants"], list)
    assert isinstance(activity["max_participants"], int)


def test_activity_description_field_populated(client):
    """Test that activity description is properly populated - AAA Pattern
    
    Arrange: client fixture provides activities
    Act: Fetch specific activity
    Assert: Verify description is not empty
    """
    # Arrange: client fixture provides clean test state

    # Act: Fetch activities
    response = client.get("/activities")
    data = response.json()

    # Assert: Each activity has a description
    for activity_name, activity_data in data.items():
        assert len(activity_data["description"]) > 0
        assert isinstance(activity_data["description"], str)


def test_activity_participants_count_accurate(client):
    """Test that participants count matches list length - AAA Pattern
    
    Arrange: client fixture provides activities with known participants
    Act: Fetch activities
    Assert: Verify participants list is accurate
    """
    # Arrange: Chess Club has 1 participant, Gym Class has 0

    # Act: Fetch activities
    response = client.get("/activities")
    data = response.json()

    # Assert: Check participant counts
    assert len(data["Chess Club"]["participants"]) == 1
    assert "michael@mergington.edu" in data["Chess Club"]["participants"]
    assert len(data["Gym Class"]["participants"]) == 0
