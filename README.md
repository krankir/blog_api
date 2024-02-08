# blog_api
## Описание
REST API для работы с блогом

### Технологии
- Python
- Postgresql
- Django REST Framework
- Docker
- Celery
- Redis

### Шаблон наполнения .env файла
- работаем с postgresql
```
DB_ENGINE=django.db.backends.postgresql 
```
- имя базы данных
```
DB_NAME=postgres
```
- пользователь базы данных
```
POSTGRES_USER=postgres
```
- пароль пользователя базы данных
```
POSTGRES_PASSWORD=postgres
```
- название контейнера
```
DB_HOST=db
```
- порт для работы с базой данных
```
DB_PORT=5432
```

### Запуск проекта в контейнерах Docker
- Перейдите в раздел infra для сборки docker-compose
```
docker-compose up -d --build 
```
- Выполнить migrate
```
docker-compose exec web python manage.py migrate
```
- Создайте пользователя
```
docker-compose exec web python manage.py createsuperuser
```
- (или) Сменить пароль для пользователя admin
```
docker-compose exec web python manage.py changepassword admin
```
- Сформируйте STATIC файлы:
```
docker-compose exec web python manage.py collectstatic --no-input
```

# Реализованные API endpoints:
- **Подписка на пользователя.**
```
Пользователь отправляет POST-запрос с телом запроса  {"username": "rest_user"},  на `api/v1/auth/users/subscribe/`
```
- **Отписка от пользователя.**
```
Пользователь отправляет DELETE-запрос с телом запроса  {"username": "rest_user"}, на `api/v1/auth/users/subscribe/`
```
- **Просмотр всех на кого подписан пользователь.**
```
Пользователь отправляет GET-запрос `api/v1/auth/users/subscriptions/`
```
- **Персональная лента новостей пользователя.**
```
Пользователь отправляет GET-запрос `api/v1/auth/users/newsfeed/`
```
- **Пользователь помечает пост в ленте как прочитанный.**
```
Пользователь отправляет POST-запрос по эндпоинту api/v1/posts/mark_read с передачей в теле запроса id сообщения  {"id": 1}
```


### Автор
Анатолий Редько

### License
MIT
# blog_api