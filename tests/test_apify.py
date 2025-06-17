from unittest.mock import patch, MagicMock
import subprocess


@patch("backend.main.client.actor")
@patch("backend.main.client.dataset")
@patch("backend.main.init_db")
@patch("backend.main.subprocess.run")
def test_successful_apify_scraping(mock_subprocess_run, mock_init_db, mock_dataset, mock_actor, client):
    mock_subprocess_run.return_value = None

    fake_run = {"defaultDatasetId": "fake_dataset"}
    fake_items = [{"fullText": "Mocked tweet", "createdAt": "2025-03-30T20:00:00Z"}]

    mock_actor.return_value.call.return_value = fake_run
    mock_dataset.return_value.iterate_items.return_value = fake_items

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [1]
    mock_init_db.return_value = mock_conn

    response = client.post('/scrape', json={"hashtags": ["python"], "platforms": ["twitter"]})

    assert response.status_code == 201
    print(response.json)
    assert response.json["result"][0]["content"] == "Mocked tweet"


@patch("backend.main.client.actor", side_effect=Exception("Apify down"))
@patch("backend.main.subprocess.run")
def test_apify_failure(mock_subprocess_run, mock_actor, client):
    mock_subprocess_run.return_value = None

    response = client.post('/scrape', json={"hashtags": ["python"], "platforms": ["twitter"]})
    assert response.status_code == 500
    assert "Apify down" in response.json["error"]


@patch("backend.main.client.actor")
@patch("backend.main.client.dataset")
@patch("backend.main.init_db")
@patch("backend.main.subprocess.run")
def test_no_posts_found(mock_subprocess_run, mock_init_db, mock_dataset, mock_actor, client):
    mock_subprocess_run.return_value = None

    fake_run = {"defaultDatasetId": "fake_dataset"}
    fake_items = []

    mock_actor.return_value.call.return_value = fake_run
    mock_dataset.return_value.iterate_items.return_value = fake_items

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_init_db.return_value = mock_conn

    response = client.post('/scrape', json={"hashtags": ["empty"], "platforms": ["twitter"]})
    assert response.status_code == 201
    assert response.json["result"] == []


@patch("backend.main.subprocess.run")
@patch("backend.main.client.actor")
@patch("backend.main.client.dataset")
@patch("backend.main.psycopg2.connect")
def test_error_storing_captions(mock_connect, mock_dataset, mock_actor, mock_subprocess_run, client):
    mock_subprocess_run.return_value = None

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.execute.side_effect = Exception("Database write failed")
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    fake_run = {"defaultDatasetId": "mock_dataset"}
    mock_dataset.return_value.iterate_items.return_value = [
        {"fullText": "some tweet", "createdAt": "2024-01-01T00:00:00Z"}
    ]

    actor_instance = MagicMock()
    actor_instance.call.return_value = fake_run
    mock_actor.return_value = actor_instance

    response = client.post('/scrape', json={"hashtags": ["python"], "platforms": ["twitter"]})
    assert response.status_code == 500
    assert "Database operation failed" in response.json["error"]
