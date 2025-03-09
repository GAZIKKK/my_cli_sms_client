import toml
import socket
import logging
import sys
from base64 import b64encode
import json
from typing import Dict
from http_client import *

# Настраиваем логирование
logging.basicConfig(
    filename="sms_client.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


def load_config(config_path: str) -> Dict:
    """Загружает конфигурацию из файла TOML."""
    try:
        with open(config_path, "r") as f:
            return toml.load(f)
    except FileNotFoundError:
        logging.error("Файл конфигурации не найден")
        sys.exit("Ошибка: файл конфигурации не найден")


def create_http_request(sender: str, recipient: str, message: str, config: Dict) -> bytes:
    """Создаёт HTTP-запрос в виде байтов."""
    auth_header = b64encode(f"{config['auth']['username']}:{config['auth']['password']}".encode()).decode()
    body = json.dumps({
        "sender": sender,
        "recipient": recipient,
        "message": message,
    })

    host = config["api"]["host"]
    port = config["api"]["port"]

    headers = {
        "Host": f"{host}:{port}",
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/json",
        "Content-Length": str(len(body)),
    }

    request = HttpRequest("POST", "/send_sms", headers, body)
    return request.to_bytes()


def send_sms(sender: str, recipient: str, message: str, config: Dict):
    """Отправляет HTTP-запрос через сокет и обрабатывает ответ."""
    host = config["api"]["host"]
    port = config["api"]["port"]

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)  # Таймаут для избежания зависаний
            s.connect((host, port))
            request = create_http_request(sender, recipient, message, config)
            s.sendall(request)

            response_data = s.recv(4096)
            if not response_data:
                logging.error("Сервер не прислал данных в ответ")
                print("Ошибка: Пустой ответ от сервера")
                return

            http_response = HttpResponse.from_bytes(response_data)

        # Обрабатываем JSON-ответ
        try:
            response_json = json.loads(http_response.body)
        except json.JSONDecodeError:
            logging.error(f"Ошибка декодирования JSON: {http_response.body}")
            print(f"Ошибка: Некорректный JSON-ответ от сервера: {http_response.body}")
            return

        # Обрабатываем возможные коды ответа
        if http_response.status_code == 200:
            print(f"Сообщение успешно отправлено! ID: {response_json.get('message_id')}")
        elif http_response.status_code == 400:
            print(f"Ошибка: Некорректные параметры - {response_json.get('error', 'Неизвестная ошибка')}")
        elif http_response.status_code == 401:
            print("Ошибка: Неверные учетные данные (401 Unauthorized)")
        elif http_response.status_code == 500:
            print("Ошибка: Внутренняя ошибка сервера (500 Internal Server Error)")
        else:
            print(f"Неожиданный ответ: {http_response.status_code} - {response_json}")

        logging.info(f"Ответ сервера ({http_response.status_code}): {response_json}")

    except socket.timeout:
        logging.error("Ошибка: Таймаут соединения")
        print("Ошибка: Превышено время ожидания ответа от сервера")
    except socket.error as e:
        logging.error(f"Ошибка сокета: {e}")
        print(f"Ошибка: {e}")
