from typing import Dict


class HttpRequest:
    """Класс для формирования HTTP-запроса."""

    def __init__(self, method: str, path: str, headers: Dict[str, str], body: str):
        self.method = method
        self.path = path
        self.headers = headers
        self.body = body

    def to_bytes(self) -> bytes:
        """Преобразует объект HTTP-запроса в байтовую строку."""
        request_line = f"{self.method} {self.path} HTTP/1.1\r\n"
        headers = "".join(f"{key}: {value}\r\n" for key, value in self.headers.items())
        full_request = request_line + headers + "\r\n" + self.body  # Добавлен \r\n перед телом
        return full_request.encode("utf-8")


class HttpResponse:
    """Класс для парсинга HTTP-ответа."""

    def __init__(self, status_code: int, headers: Dict[str, str], body: str):
        self.status_code = status_code
        self.headers = headers
        self.body = body

    @classmethod
    def from_bytes(cls, binary_data: bytes) -> "HttpResponse":
        """Парсит HTTP-ответ из байтовой строки."""
        decoded = binary_data.decode("utf-8", errors="replace")
        lines = decoded.split("\r\n")

        if len(lines) < 1:
            raise ValueError("Некорректный HTTP-ответ")

        # Первая строка - статус ответа
        status_parts = lines[0].split(" ", 2)
        if len(status_parts) < 2:
            raise ValueError("Ошибка парсинга HTTP-статуса")

        _, status_code, _ = status_parts

        headers = {}
        body_index = 0
        for i, line in enumerate(lines[1:], start=1):
            if line == "":
                body_index = i + 1
                break
            if ": " in line:
                key, value = line.split(": ", 1)
                headers[key] = value

        body = "\r\n".join(lines[body_index:])
        return cls(int(status_code), headers, body)
