import pytest
from app import create_app
from app.container import create_container
from app.models import Base, get_engine

@pytest.fixture()
def test_client(tmp_path):
    db_file = tmp_path / "test_db.sqlite"
    db_url = f"sqlite:///{db_file}"

    container = create_container()
    container.config.DATABASE_URL = db_url

    engine = get_engine(db_url)
    Base.metadata.create_all(engine)

    app = create_app(container)
    app.testing = True

    with app.test_client() as client:
        yield client

def test_user_and_task_crud(test_client):
    resp = test_client.post('/users/', json={'username': 'jan', 'role': 'user'})
    assert resp.status_code == 201
    user = resp.get_json()
    user_id = user['id']

    resp = test_client.post('/tasks/', json={
        'task_name': 'kupić warzywa',
        'user_id': user_id,
        'priority': 'high'
    })
    assert resp.status_code == 201
    task = resp.get_json()
    task_id = task['task_id']

    resp = test_client.get('/tasks/')
    assert resp.status_code == 200
    tasks = resp.get_json()
    assert len(tasks) == 1

    resp = test_client.patch(f'/tasks/{task_id}', json={'status': 'completed'})
    assert resp.status_code == 200
    updated = resp.get_json()
    assert updated['status'] == 'completed'

    resp = test_client.delete(f'/tasks/{task_id}')
    assert resp.status_code == 204

    resp = test_client.get(f'/tasks/{task_id}')
    assert resp.status_code == 404

def test_create_task_with_invalid_user(test_client):
    resp = test_client.post('/tasks/', json={
        'task_name': 'test',
        'user_id': 999
    })
    assert resp.status_code == 404
    assert 'User not found' in resp.get_data(as_text=True)
