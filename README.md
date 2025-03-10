# CLI-клиент для отправки SMS-сообщений

Этот проект представляет собой CLI-программу. Программа является клиентом к условному сервису отправки SMS-сообщений, реализованному в соответствии со спецификацией `sms-platform.yaml`.

## Требования

- Python 3.8+
- Установленный Prism для запуска мок-сервера (см. раздел "Установка Prism")
- Файл конфигурации `config.toml` (см. раздел "Конфигурация")
- Спецификация API `sms-platform.yaml` (должна быть в папке с Prism)

## Установка

### Установка Prism
Перед запуском программы необходимо скачать и настроить Prism для эмуляции сервера SMS-платформы:

1. Скачайте Prism для своей платформы:
   - Windows / Linux / macOS: [https://github.com/stoplightio/prism/releases](https://github.com/stoplightio/prism/releases)
2. Создайте папку (например, `my_server`), поместите в неё скачанный файл Prism (например, `prism-cli-win.exe`) и файл `sms-platform.yaml`.
3. В терминале перейдите в эту папку и выполните команду для запуска мок-сервера:
   ```bash
   prism-cli-win.exe mock sms-platform.yaml
4. После этого API будет доступно по адресу http://localhost:4010/send_sms

## Запуск программы
1. Установите необходимую библиотеку TOML для работы с конфигурацией: 
pip install toml
2. Запустите программу через командную строку, указав необходимые параметры: 
python main.py 231 231 "Привет!" --config config.toml
3. Программа записывает информацию о своей работе в файл sms_client.log
