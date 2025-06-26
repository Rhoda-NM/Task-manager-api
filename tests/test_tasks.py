def test_create_tasks(client, access_token):
    """Test creating a new task."""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.post('/tasks/', json={
        'title': 'Test Task',
        'description': 'This is a test task.',
        'completed': False,
        'due_date': '2023-12-31T23:59:59',
        'priority': 'Medium'
    }, headers=headers)

    assert response.status_code == 201
    assert response.json['title'] == 'Test Task'

def test_get_tasks(client, access_token):
    """Test getting all tasks."""
    headers = {'Authorization': f'Bearer {access_token}'}
    client.post('/tasks/', json={
        'title': 'Test Task 1'}, headers=headers)
    client.post('/tasks/', json={
        'title': 'Test Task 2'}, headers=headers)
    
    response = client.get('/tasks/', headers=headers)
    assert response.status_code == 200
    assert len(response.json['tasks']) >= 2
    