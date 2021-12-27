## Описание проекта:
Социальная сеть Yatube для публикации дневников. Учебный проект, разработан по классической MVT архитектуре. Используется пагинация постов и кэширование.
Регистрация реализована с верификацией данных, сменой и восстановлением пароля через почту.
Написаны тесты, проверяющие работу сервиса.

## Установка и запуск проекта:
Клонировать репозиторий и перейти в него в командной строке (испольщуем ssh):
```
git clone git@github.com:Slavchick12/api_yatube.git
```
```
cd api_yatube
```
Cоздать и активировать виртуальное окружение:
```
python3 -m venv venv
```
```
source venv/bin/activate (for Linux)
```
Обновить pip до последней версии:
```
python3 -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

Выполнить миграции:
```
python3 manage.py migrate
```
Запустить проект:
```
python3 manage.py runserver
```
## Примеры использования API:
Детальное описание и примеры работы API проекта представлены в 
документации: http://127.0.0.1:8000/redoc/ в формате ReDoc.
Используется:
Python 3, Django, PostgreSQL, Gunicorn, Nginx, Yandex.Cloud (Ubuntu 20.04 LTS), unittest.
