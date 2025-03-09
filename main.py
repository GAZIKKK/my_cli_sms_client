import argparse
from send_sms import load_config, send_sms


def main():
    # Парсим аргументы командной строки
    parser = argparse.ArgumentParser(description="CLI клиент для отправки СМС.")
    parser.add_argument("sender", help="Номер отправителя")
    parser.add_argument("recipient", help="Номер получателя")
    parser.add_argument("message", help="Текст сообщения")
    parser.add_argument(
        "--config",
        default="config.toml",
        help="Путь к файлу конфигурации (по умолчанию: config.toml)",
    )

    args = parser.parse_args()

    # Загружаем конфигурацию
    config = load_config(args.config)

    # Отправляем SMS
    send_sms(args.sender, args.recipient, args.message, config)


if __name__ == "__main__":
    main()
