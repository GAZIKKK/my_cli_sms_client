import pytest
from http_client import HttpRequest, HttpResponse


def test_http_request_to_bytes():
    """Тестирует преобразование объекта HttpRequest в байты."""
    request = HttpRequest(
        "POST",
        "/send_sms",
        {"Host": "localhost:4010", "Content-Type": "application/json"},
        '{"message": "test"}'
    )
    request_bytes = request.to_bytes().decode()

    assert request_bytes.startswith("POST /send_sms HTTP/1.1\r\n")
    assert "Host: localhost:4010\r\n" in request_bytes
    assert "Content-Type: application/json\r\n" in request_bytes
    assert request_bytes.endswith('{"message": "test"}')


def test_http_response_from_bytes():
    """Тестирует разбор HTTP-ответа из байтов."""
    response_bytes = b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{\"status\": \"success\"}"
    response = HttpResponse.from_bytes(response_bytes)

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.body == '{"status": "success"}'


def test_http_response_invalid():
    """Тестирует обработку некорректного HTTP-ответа."""
    with pytest.raises(ValueError):
        HttpResponse.from_bytes(b"INVALID RESPONSE")
