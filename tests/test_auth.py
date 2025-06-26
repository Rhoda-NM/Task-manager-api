def test_register_user(client):
    """Test user registration."""
    response = client.post('/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword'
    })
    assert response.status_code == 201
    assert response.json["username"] == 'testuser'

def test_login_user(client):
    """Test user login."""
    # First, register a user
    client.post('/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword'
    })

    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'testpassword'
    })

    assert response.status_code == 200
    assert 'access_token' in response.json

