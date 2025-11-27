# Auth System (Test Assignment)

Система аутентификации с ролями и правами доступа.  
Пользователи могут регистрироваться, логиниться, обновлять профиль и удалять аккаунт.  
Пример бизнес-объектов: Клиенты, Заказы, Товары.  
Роли: admin, manager.

---

## Запуск

```bash
git clone <repo_url>
cd auth_system
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata fixtures/initial_data.json
python manage.py runserver

## Тестовый пользователь

Email: admin@example.com
Пароль: 123456

Важно: в фикстурах хранится хеш пароля (password_hash).
Если меняешь пароль вручную — генерируй через Django:

from django.contrib.auth.hashers import make_password
print(make_password("новый_пароль"))

### Проверка API (Windows curl)

Login и получение JWT:

curl -X POST "http://127.0.0.1:8000/api/users/login/" ^
-H "Content-Type: application/json" ^
-d "{\"email\":\"admin@example.com\",\"password\":\"123456\"}"

Просмотр профиля:

curl -X GET "http://127.0.0.1:8000/api/users/me/" ^
-H "Authorization: Bearer <JWT_TOKEN>"

Просмотр бизнес-объектов:

curl -X GET "http://127.0.0.1:8000/api/business/elements/" ^
-H "Authorization: Bearer <JWT_TOKEN>"


Автор: Марат Ахметов
Email: akhmetovmarat1992@yandex.ru