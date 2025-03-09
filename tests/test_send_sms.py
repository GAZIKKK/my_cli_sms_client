import pytest
import json
from base64 import b64encode
from send_sms import create_http_request, send_sms


def test_create_http_request():
    """Тестирует создание HTTP-запроса для отправки СМС."""
    config = {
        "auth": {"username": "testuser", "password": "testpass"},
        "api": {"host": "localhost", "port": 4010}
    }

    request_bytes = create_http_request("+1234567890", "+0987654321", "Hello!", config)
    request_str = request_bytes.decode()

    assert request_str.startswith("POST /send_sms HTTP/1.1\r\n")
    assert "Host: localhost:4010\r\n" in request_str
    assert "Authorization: Basic" in request_str  # Проверяем, что заголовок авторизации есть
    assert "Content-Type: application/json\r\n" in request_str

    # Проверяем, что тело запроса содержит правильные данные
    body = request_str.split("\r\n\r\n", 1)[1]
    json_body = json.loads(body)
    assert json_body["sender"] == "+1234567890"
    assert json_body["recipient"] == "+0987654321"
    assert json_body["message"] == "Hello!"


@pytest.fixture
def mock_socket(monkeypatch):
    """Мок для socket.socket, который не делает реального сетевого соединения."""

    class MockSocket:
        def __init__(self, *args, **kwargs):
            self.data_sent = b""

        def connect(self, address):
            pass  # Ничего не делаем

        def sendall(self, data):
            self.data_sent = data  # Сохраняем отправленные данные

        def recv(self, buffer_size):
            return b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{\"status\": \"success\", \"message_id\": \"12345\"}"

        def close(self):
            pass  # Ничего не делаем

        def settimeout(self, timeout):
            pass  # Просто заглушка для совместимости

        def __enter__(self):
            return self  # Возвращаем сам объект для использования в with-блоке

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass  # Ничего не делаем при выходе из with-блока

    monkeypatch.setattr("socket.socket", lambda *args, **kwargs: MockSocket())


def test_send_sms(mock_socket, capsys):
    """Тестирует отправку СМС без реального соединения."""
    config = {
        "auth": {"username": "testuser", "password": "testpass"},
        "api": {"host": "localhost", "port": 4010}
    }

    send_sms("+1234567890", "+0987654321", "Hello!", config)

    # Проверяем, что в stdout есть сообщение об успешной отправке
    captured = capsys.readouterr()
    assert "Сообщение успешно отправлено! ID: 12345" in captured.out
