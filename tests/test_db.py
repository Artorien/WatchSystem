import pytest
from backend.main import app as flask_app, init_db
from unittest.mock import patch


@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    return flask_app.test_client()


def test_init_db_success(monkeypatch):
    monkeypatch.setenv('DB_NAME', 'test_db')
    monkeypatch.setenv('DB_USER', 'test_user')
    monkeypatch.setenv('DB_PASSWORD', 'test_password')

    with patch('backend.main.psycopg2.connect') as mock_connect:
        init_db()
        mock_connect.assert_called_with(
            dbname='test_db',
            user='test_user',
            password='test_password',
            host='db',
            port='5432'
        )


def test_init_db_no_password(monkeypatch):
    monkeypatch.setenv('DB_NAME', 'test_db')
    monkeypatch.setenv('DB_USER', 'test_user')
    monkeypatch.setenv('DB_PASSWORD', '')

    with pytest.raises(ValueError) as excinfo:
        init_db()
    assert "Database password is missing" in str(excinfo.value)


def test_db_connection_failure_during_scraping(client):
    with patch("backend.main.client.actor") as mock_actor:
        with patch("backend.main.psycopg2.connect", side_effect=Exception("Dataset was not found")):
            response = client.post('/scrape', json={"hashtags": ["python"], "platforms": ["twitter"]})
            assert response.status_code == 500
            assert "Dataset was not found" in response.json["error"]


# TODO: Add OpenAi API key, test is failing due to its absence
# def test_db_write_failure_during_caption_store(client):
#     mock_conn = MagicMock()
#     mock_cursor = MagicMock()
#     mock_cursor.execute.side_effect = Exception("Failed to insert data")
#     mock_conn.cursor.return_value = mock_cursor
#
#     with patch("app.psycopg2.connect", return_value=mock_conn):
#         mock_run = {"defaultDatasetId": "mock_dataset"}
#         mock_dataset = MagicMock()
#         mock_dataset.iterate_items.return_value = [
#             {"fullText": "some tweet", "createdAt": "2024-01-01T00:00:00Z"}
#         ]
#
#         with patch("app.client.actor") as mock_actor:
#             actor_instance = MagicMock()
#             actor_instance.call.return_value = mock_run
#             mock_actor.return_value = actor_instance
#
#             with patch("app.client.dataset", return_value=mock_dataset):
#                 response = client.post('/scrape', json={"hashtags": ["python"], "platforms": ["twitter"]})
#                 assert response.status_code == 500
#                 assert "Database operation failed." in response.json["error"]
