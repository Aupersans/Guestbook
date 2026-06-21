import sys
import os
import pytest
from app import app
from database import get_db_connection

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        conn = get_db_connection()
        conn.execute('DELETE FROM messages')
        conn.execute("DELETE FROM sqlite_sequence WHERE name='messages'")
        conn.commit()
        conn.close()
        yield client

@pytest.fixture
def auth_client(client):
    client.post('/login', data={
        'username': 'admin',
        'password': '123'
    })
    return client