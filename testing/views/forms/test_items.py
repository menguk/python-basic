def test_items_detail(client):
    url = '/items/10/'
    response = client.get(url)
    assert response.status_code == 200