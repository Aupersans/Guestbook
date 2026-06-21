def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'Гостевая книга' in response.get_data(as_text=True)

def test_add_message(client):
    client.post('/add', data={
        'name': 'Тест',
        'message': 'Привет!'
    })
    response = client.get('/')
    data = response.get_data(as_text=True)
    assert 'Тест' in data
    assert 'Привет!' in data

def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200
    data = response.get_data(as_text=True)
    assert 'Вход' in data
    assert 'username' in data