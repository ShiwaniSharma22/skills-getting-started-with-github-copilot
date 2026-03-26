"""Tests for signup endpoint using AAA (Arrange-Act-Assert) pattern"""


def test_successful_signup(client):
    """Test successful signup - AAA Pattern
    
    Arrange: Set up test data (activity exists, email not registered)
    Act: Perform signup
    Assert: Verify success and state changed
    """
    # Arrange: Gym Class exists and has capacity, email is not registered
    email = "john@mergington.edu"
    activity = "Gym Class"

    # Act: Perform signup
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert: Verify success and state changed
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

    # Verify participant was added
    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity]["participants"]


def test_duplicate_signup_fails(client):
    """Test duplicate signup rejection - AAA Pattern
    
    Arrange: Student already registered
    Act: Try to sign up again
    Assert: Verify rejection with appropriate error
    """
    # Arrange: michael@mergington.edu already registered for Chess Club
    email = "michael@mergington.edu"
    activity = "Chess Club"

    # Act: Try to sign up again
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert: Verify rejection
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_nonexistent_activity_signup_fails(client):
    """Test signup for non-existent activity - AAA Pattern
    
    Arrange: Activity doesn't exist
    Act: Try to sign up
    Assert: Verify 404 error
    """
    # Arrange: Activity doesn't exist
    email = "test@mergington.edu"
    activity = "Nonexistent Club"

    # Act: Try to sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert: Verify 404 error
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_at_capacity_fails(client):
    """Test signup when activity is full - AAA Pattern
    
    Arrange: Activity has max 2 participants, already has 1
    Act: Sign up to fill capacity, then try one more
    Assert: Verify rejection due to capacity
    """
    # Arrange: Chess Club has max_participants=2, participants=["michael@mergington.edu"]

    # Act: Sign up first new participant to reach capacity
    response1 = client.post("/activities/Chess Club/signup?email=alice@mergington.edu")
    assert response1.status_code == 200

    # Try to sign up when at capacity
    response2 = client.post("/activities/Chess Club/signup?email=bob@mergington.edu")

    # Assert: Verify rejection due to capacity
    assert response2.status_code == 400
    assert "maximum capacity" in response2.json()["detail"]


def test_multiple_signups_allowed(client):
    """Test multiple students can sign up for same activity - AAA Pattern
    
    Arrange: Activity "Gym Class" has capacity 2, is empty
    Act: Sign up two students
    Assert: Both succeed and are in participants
    """
    # Arrange: Gym Class has capacity 2, is empty
    activity = "Gym Class"
    email1 = "alice@mergington.edu"
    email2 = "bob@mergington.edu"

    # Act: Sign up first student
    response1 = client.post(f"/activities/{activity}/signup?email={email1}")

    # Act: Sign up second student
    response2 = client.post(f"/activities/{activity}/signup?email={email2}")

    # Assert: Both succeed
    assert response1.status_code == 200
    assert response2.status_code == 200

    # Verify both are in participants
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity]["participants"]
    assert email1 in participants
    assert email2 in participants
    assert len(participants) == 2


def test_signup_boundary_condition(client):
    """Test signup at exactly n-1 capacity - AAA Pattern
    
    Arrange: Activity with capacity of 3, has 1 participant
    Act: Sign up to reach exactly capacity
    Assert: Signup succeeds and reaches max
    """
    # Arrange: Programming Class has max_participants=3, participants=["emma@mergington.edu"]
    activity = "Programming Class"
    email1 = "alice@mergington.edu"
    email2 = "bob@mergington.edu"

    # Act: Sign up first student (reaches 2 of 3)
    response1 = client.post(f"/activities/{activity}/signup?email={email1}")
    assert response1.status_code == 200

    # Act: Sign up second student (reaches 3 of 3 - at capacity)
    response2 = client.post(f"/activities/{activity}/signup?email={email2}")

    # Assert: Both succeed and activity is now at max
    assert response2.status_code == 200
    activities_response = client.get("/activities")
    assert len(activities_response.json()[activity]["participants"]) == 3


def test_signup_response_contains_message(client):
    """Test signup response contains confirmation message - AAA Pattern
    
    Arrange: Activity and email ready for signup
    Act: Perform signup
    Assert: Response contains descriptive message
    """
    # Arrange: Gym Class available
    email = "carol@mergington.edu"
    activity = "Gym Class"

    # Act: Sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert: Response contains proper message format
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]
