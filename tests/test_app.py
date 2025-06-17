def test_scrape_missing_hashtag(client):
    response = client.post('/scrape', json={"platforms": ["twitter"]})
    assert response.status_code == 400
    assert response.json['error'] == "Missing 'hashtags'"


def test_scrape_missing_platforms(client):
    response = client.post('/scrape', json={"hashtags": ["test"]})
    assert response.status_code == 400
    assert response.json['error'] == "Missing or invalid 'platforms' list"


def test_scrape_invalid_platform(client):
    response = client.post('/scrape', json={"hashtags": ["python"], "platforms": ["linkedin"]})
    assert response.status_code == 400
    assert "Invalid platform" in response.json["error"]


def test_valid_hashtags_twitter(client):
    response = client.post('/scrape', json={"hashtags": ["python"], "platforms": ["twitter"]})
    assert response.status_code in [200, 500]


def test_scrape_missing_platforms_again(client):
    response = client.post('/scrape', json={"hashtags": ["python"]})
    assert response.status_code == 400
    assert response.json['error'] == "Missing or invalid 'platforms' list"


def test_scrape_invalid_platform_again(client):
    response = client.post('/scrape', json={"hashtags": ["python"], "platforms": ["linkedin"]})
    assert response.status_code == 400
    assert "Invalid platform" in response.json["error"]
