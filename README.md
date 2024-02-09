# blog_api
## Описание
REST API для работы с блогом. Реализован функционал для пользователей подписавшихся на рассылку на почту прилетает подборка из 5 последних постов ленты.
Установлен лимит на количество запросов в день. Для авторизованных 1000 в день, а для анонимных пользователей 100 запросов в день.

### Технологии
- Python
- Postgresql
- Django REST Framework
- Docker
- Celery
- Redis

### Создать в корне проекта файл .env и заполнить тестовыми данными.
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
- Создайте пользователя
```
docker-compose exec web python manage.py createsuperuser
```
- (или) Сменить пароль для пользователя admin
```
docker-compose exec web python manage.py changepassword admin
```

#### Админ понель будеть доступна по адресу: [127.0.0.1/admin](http://127.0.0.1/admin)

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