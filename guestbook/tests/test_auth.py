def test_login_success(client):
    response = client.post('/login', data={
        'username': 'admin',
        'password': '123'
    })
    assert response.status_code == 302
    with client.session_transaction() as sess:
        assert sess.get('logged_in') is True
        assert sess.get('username') == 'admin'

def test_login_failure(client):
    response = client.post('/login', data={
        'username': 'admin',
        'password': 'wrong'
    })
    assert response.status_code == 200
    assert 'Неверный логин или пароль' in response.get_data(as_text=True)
    with client.session_transaction() as sess:
        assert sess.get('logged_in') is None

def test_delete_without_auth(client):
    client.post('/add', data={
        'name': 'Тест',
        'message': 'Сообщение для удаления'
    })
    response = client.get('/delete/1')
    assert response.status_code == 302
    response = client.get('/')
    assert 'Сообщение для удаления' in response.get_data(as_text=True)

def test_delete_with_auth(auth_client):
    auth_client.post('/add', data={
        'name': 'Тест',
        'message': 'Сообщение для удаления'
    })
    response = auth_client.get('/delete/1')
    assert response.status_code == 302
    response = auth_client.get('/')
    assert 'Сообщение для удаления' not in response.get_data(as_text=True)

def test_logout(client):
    client.post('/login', data={'username': 'admin', 'password': '123'})
    with client.session_transaction() as sess:
        assert sess.get('logged_in') is True
    client.get('/logout')
    with client.session_transaction() as sess:
        assert sess.get('logged_in') is None
        assert sess.get('username') is None