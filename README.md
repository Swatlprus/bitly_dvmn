# Сокращение ссылок с помощью сервиса Bitly

Программа позволяет получать сокращенные ссылки. Для этого используется API от сервиса Bit.ly

### Как установить

Python уже должен быть установлен
Затем используйте `pip` для установки зависимостей

```pip install -r requirements.txt```

Не забудьте создать файл для переменных окружения `.env` и прописать туда ваш токен от сервиса Bit.ly
Пример содержимого файла `.env`

```BITLY_TOKEN=123456789123456789```

Рекомендуется использоваться Виртуальное окружение (venv)

### Примеры использования

Команда для получения сокращенной ссылки для адреса https://yandex.ru/

```python3 main.py https://yandex.ru/```

 Команда для получения количество кликов по сокращенной ссылке (Указываем ссылку из bit.ly)

 ```python3 main.py https://bit.ly/3zxRQqw```

### Цель проекта

Учебный проект по сокращению ссылок от онлайн-курса Devman (dvmn.org)