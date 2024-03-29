## Описание проекта:
Социальная сеть Yatube для публикации дневников. Учебный проект, разработан по классической MVT архитектуре. Используется пагинация постов и кэширование.
Регистрация реализована с верификацией данных, сменой и восстановлением пароля через почту.
Написаны тесты, проверяющие работу сервиса.

## Установка и запуск проекта:
Клонировать репозиторий и перейти в него в командной строке (испольщуем ssh):
```
git clone git@github.com:Slavchick12/yatube.git
```
```
cd yatube
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
## Используется:
```
Python 3.9, Django 2.2, unittest.
```
