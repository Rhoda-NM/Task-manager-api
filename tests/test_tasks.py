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

def  test_update_task(client, access_token):
    """Test updating a task."""
    headers = {'Authorization': f'Bearer {access_token}'}
    create_response = client.post('/tasks/', json={
        'title': 'Task to Update',
        'description': 'This task will be updated.',
        'completed': False,
        'due_date': '2023-12-31T23:59:59',
        'priority': 'Low'
    }, headers=headers) 

    task_id = create_response.json['id']

    update_response = client.put(f'/tasks/{task_id}', json={
        'title': 'Updated Task',
        'description': 'This task has been updated.',
        'completed': True,
        'due_date': '2024-01-01T00:00:00',
        'priority': 'High'
    }, headers=headers)

    assert update_response.status_code == 200
    assert update_response.json['title'] == 'Updated Task'  
    assert update_response.json['completed'] is True
    assert update_response.json['priority'] == 'High'

def test_delete_task(client, access_token):
    """Test deleting a task."""
    headers = {'Authorization': f'Bearer {access_token}'}
    create_response = client.post('/tasks/', json={
        'title': 'Task to Delete',
        'description': 'This task will be deleted.',
        'completed': False,
        'due_date': '2023-12-31T23:59:59',
        'priority': 'Medium'
    }, headers=headers)

    task_id = create_response.json['id']

    delete_response = client.delete(f'/tasks/{task_id}', headers=headers)
    
    assert delete_response.status_code == 204

    # Verify the task is deleted
    get_response = client.get(f'/tasks/{task_id}', headers=headers)
    assert get_response.status_code == 404