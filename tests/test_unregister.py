"""Tests for unregister endpoint using AAA (Arrange-Act-Assert) pattern"""


def test_successful_unregister(client):
    """Test successful unregister - AAA Pattern
    
    Arrange: Student is registered
    Act: Unregister
    Assert: Verify success and participant removed
    """
    # Arrange: michael@mergington.edu is registered for Chess Club
    email = "michael@mergington.edu"
    activity = "Chess Club"

    # Act: Unregister
    response = client.delete(f"/activities/{activity}/unregister?email={email}")

    # Assert: Verify success and participant removed
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]

    # Verify participant was removed
    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity]["participants"]


def test_unregister_not_registered_fails(client):
    """Test unregister for non-registered student - AAA Pattern
    
    Arrange: Student not registered
    Act: Try to unregister
    Assert: Verify rejection
    """
    # Arrange: notregistered@mergington.edu is not registered
    email = "notregistered@mergington.edu"
    activity = "Chess Club"

    # Act: Try to unregister
    response = client.delete(f"/activities/{activity}/unregister?email={email}")

    # Assert: Verify rejection
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]


def test_unregister_nonexistent_activity_fails(client):
    """Test unregister from non-existent activity - AAA Pattern
    
    Arrange: Activity doesn't exist
    Act: Try to unregister
    Assert: Verify 404 error
    """
    # Arrange: Activity doesn't exist
    email = "michael@mergington.edu"
    activity = "Nonexistent Club"

    # Act: Try to unregister
    response = client.delete(f"/activities/{activity}/unregister?email={email}")

    # Assert: Verify 404 error
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_frees_capacity(client):
    """Test that unregistering frees up capacity for new signup - AAA Pattern
    
    Arrange: Chess Club at capacity (max 2, has 1 registered)
    Act: Fill to capacity, unregister, then signup again
    Assert: New signup succeeds after unregister
    """
    # Arrange: Chess Club max_participants=2, has michael@mergington.edu
    activity = "Chess Club"
    new_student1 = "alice@mergington.edu"
    new_student2 = "bob@mergington.edu"
    original_student = "michael@mergington.edu"

    # Act: Fill to capacity
    client.post(f"/activities/{activity}/signup?email={new_student1}")
    capacity_response = client.post(f"/activities/{activity}/signup?email={new_student2}")
    assert capacity_response.status_code == 400  # Verify it's at capacity

    # Act: Unregister original student
    unregister_response = client.delete(
        f"/activities/{activity}/unregister?email={original_student}"
    )

    # Assert: Unregister succeeds
    assert unregister_response.status_code == 200

    # Act: Try to sign up after unregister
    signup_response = client.post(f"/activities/{activity}/signup?email={new_student2}")

    # Assert: Now succeeds because space is freed
    assert signup_response.status_code == 200


def test_unregister_response_contains_message(client):
    """Test unregister response contains confirmation message - AAA Pattern
    
    Arrange: Registered student ready for unregister
    Act: Unregister
    Assert: Response contains descriptive message
    """
    # Arrange: michael@mergington.edu registered for Chess Club
    email = "michael@mergington.edu"
    activity = "Chess Club"

    # Act: Unregister
    response = client.delete(f"/activities/{activity}/unregister?email={email}")

    # Assert: Response contains proper message format
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]
    assert "Unregistered" in data["message"]


def test_unregister_multiple_participants(client):
    """Test unregister when activity has multiple participants - AAA Pattern
    
    Arrange: Activity with multiple participants
    Act: Unregister one participant
    Assert: Only that participant is removed, others remain
    """
    # Arrange: Sign up multiple students to Gym Class
    activity = "Gym Class"
    email1 = "alice@mergington.edu"
    email2 = "bob@mergington.edu"

    client.post(f"/activities/{activity}/signup?email={email1}")
    client.post(f"/activities/{activity}/signup?email={email2}")

    # Act: Unregister first participant
    response = client.delete(f"/activities/{activity}/unregister?email={email1}")

    # Assert: Unregister succeeds
    assert response.status_code == 200

    # Verify first participant removed, second remains
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity]["participants"]
    assert email1 not in participants
    assert email2 in participants
    assert len(participants) == 1
