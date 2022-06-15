# automated-testing-repository

### Описание
Автоматическая проверка репозитория по github url и получение уровней образовательных результатов. Репозиторий с решениями пользователей создаются из [шаблона](https://github.com/Nurijusha/solution_template).

Функционал для пользователей:
1) Просмотр всех модулей и задач
2) Отправка url github-репозитория для проверки
3) Просмотр результатов проверки с уровнями для каждого образовательного результата и рекомендациями
4) Просмотр результатов прошлых проверок с подсчетом средних значений по каждому образовательному результату

---
### Технологии
Backend:
- Python 3.10 (django, dynamic-tests)
- Python 3.9 (static-tests)
- Django 4.0.4
- Docker 20.10.14
- Docker-compose 1.29.2
- База данных PostgreSQL
- Nginx 1.21.3
- Celery 
- Redis
- Flask 2.1.1

Frontend:
- React v18.0.0

---
### Запуск докер контейнеров
1. Установите Docker.

   #### Windows или MacOS:
    * **Для Windows 10** Установите [WSL](https://docs.microsoft.com/ru-ru/windows/wsl/install-win10)
    * Скачайте и установите [Docker Desktop](https://www.docker.com/products/docker-desktop)
    * **При необходимости** настройте выделяемые ресурсы для виртуальных машин (_Settings_ -> _Resources_)
   * **Для Windows** интегрируйте Docker с дистрибутивом Linux (WSL 2) (_Settings_ -> _Resources_ -> _WSL integration_ -> _Поставить галочку и вклюить ползунок_)
   
   #### Linux:
   * Следуйте [инструкции](https://docs.docker.com/engine/install/ubuntu/)
   
2. Установите [Git](https://git-scm.com/book/ru/v2/%D0%92%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5-%D0%A3%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0-Git)
3. Склонируйте этот репозиторий в любую папку
4. В директории django-проекта ([infra](./infra)) создайте файл *.env* с переменными окружения:
```yaml
  DOMAIN=127.0.0.1 # домен сайта или ip сервера
  SITE_NAME=Automated testing repository # название сайта
  
  EMAIL_HOST_USER=test@gmail.com # почтовый ящик с которого будут отправляться письма для активации
  EMAIL_HOST_PASSWORD=qwertyuiopasdfgh # 16-значный код приложения для почтового ящика
  
  DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
  DB_NAME=postgres # имя базы данных
  POSTGRES_USER=postgres # логин для подключения к базе данных
  POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
  DB_HOST=db # название сервиса (контейнера)
  DB_PORT=5432 # порт для подключения к БД
```
**Внимание!** Для почтового ящика должен быть настроен SMTP-сервер и разрешен доступ с непроверенных приложений. В проекте используется "smtp.gmail.com". 

**UPDATE:** После 30 мая 2022 года авторизация для сторонних приложений в google только по коду приложения.
Код создается в настройках аккаунта во вкладке безопасность. Предварительно там же необходимо включить двухфакторную аутентификацию.

5. В терминале перейдите в директорию /infra, где находится файл docker-compose.yml
6. Выполните команду:
```bash
  docker-compose up -d
```
7. Для выполнения миграций и сборки статики последовательно выполните команды:
```bash
  docker-compose exec web python manage.py migrate --noinput
  docker-compose exec web python manage.py collectstatic --no-input
```
8. Для создания суперпользователя выполните команду:
```bash
   docker-compose exec web python manage.py createsuperuser
```

---
### Администрирование проекта
Проект будет доступен локально по адресу 127.0.0.1 (localhost). Весь функционал можно протестировать. 

Все доступные api описаны в двух представлениях:
- Swagger-ui - localhost/swagger/
- ReDoc - localhost/redoc/

Админская панель:
- Заходим по адресу localhost/admin
- Вводим логин и пароль суперпользователя



