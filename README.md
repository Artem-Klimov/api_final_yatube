API интерфейс для проекта KittyGram Backend предоставляет возможность взаимодействия с бэкендом приложения KittyGram, разработанного Artem-Klimov. В данной документации представлено описание доступных эндпоинтов, параметров запросов и ожидаемых ответов.

Базовый URL:

Copy code
https://api.kittygram.com
Аутентификация
API интерфейс предусматривает использование механизма аутентификации через JWT (JSON Web Token). Пользователь может получить токен аутентификации, отправив запрос на /auth/login с указанием своих учетных данных.

Вход
Метод: POST
URL: /auth/login
Описание: Вход пользователя в систему и получение токена аутентификации.

Параметры запроса:

email (обязательный) - адрес электронной почты пользователя.
password (обязательный) - пароль пользователя.
Пример запроса:

bash
Copy code
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
Ответ:

200 OK - Вход выполнен успешно. Токен аутентификации возвращается в теле ответа.
json
Copy code
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZW1haWwiOiJ1c2VyQGV4YW1wbGUuY29tIiwiaWF0IjoxNjIxNzA0MzA0LCJleHAiOjE2MjE3MTI3MDR9.qzNUNfHjQp9sQl6-xn3NUrP8e7bl-bpCYz3hS-F-Tic"
}
401 Unauthorized - Неверные учетные данные.
Пользователи
Получение информации о текущем пользователе
Метод: GET
URL: /users/me
Описание: Получение информации о текущем аутентифицированном пользователе.

Заголовки запроса:

Authorization: Bearer {token} (обязательный) - токен аутентификации.
Пример запроса:

vbnet
Copy code
GET /users/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZW1haWwiOiJ1c2VyQGV4YW1wbGUuY29tIiwiaWF0IjoxNjIxNzA0MzA0LCJleHAiOjE2MjE3MTI3MDR9.qzNUNfHjQp9sQl6-xn3NUrP8e7bl-bpCYz3hS-F-Tic
Ответ:

200 OK - Запрос выполнен успешно. Возвращается информация о пользователе.
json
Copy code
{
  "id": 1,
  "email": "user@example.com",
  "name": "John Doe",
  "avatar": "https://example.com/avatar.jpg"
}
401 Unauthorized - Неверный токен аутентификации.
Кошки
Получение списка кошек
Метод: GET
URL: /cats
Описание: Получение списка кошек.

Заголовки запроса:

Authorization: Bearer {token} (обязательный) - токен аутентификации.
Параметры запроса:

page (необязательный) - номер страницы (по умолчанию: 1).
limit (необязательный) - количество записей на странице (по умолчанию: 20).
Пример запроса:

bash
Copy code
GET /cats?page=1&limit=10
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZW1haWwiOiJ1c2VyQGV4YW1wbGUuY29tIiwiaWF0IjoxNjIxNzA0MzA0LCJleHAiOjE2MjE3MTI3MDR9.qzNUNfHjQp9sQl6-xn3NUrP8e7bl-bpCYz3hS-F-Tic
Ответ:

200 OK - Запрос выполнен успешно. Возвращается список кошек.
json
Copy code
{
  "count": 100,
  "cats": [
    {
      "id": 1,
      "name": "Fluffy",
      "age": 3,
      "breed": "Maine Coon",
      "image": "https://example.com/fluffy.jpg"
    },
    {
      "id": 2,
      "name": "Whiskers",
      "age": 2,
      "breed": "Siamese",
      "image": "https://example.com/whiskers.jpg"
    },
    // ...
  ]
}
401 Unauthorized - Неверный токен аутентификации.
Создание новой кошки
Метод: POST
URL: /cats
Описание: Создание новой кошки.

Заголовки запроса:

Authorization: Bearer {token} (обязательный) - токен аутентификации.
Параметры запроса:

name (обязательный) - имя кошки.
age (обязательный) - возраст кошки.
breed (обязательный) - порода кошки.
image (необязательный) - URL изображения кошки.
Пример запроса:

bash
Copy code
POST /cats
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZW1haWwiOiJ1c2VyQGV4YW1wbGUuY29tIiwiaWF0IjoxNjIxNzA0MzA0LCJleHAiOjE2MjE3MTI3MDR9.qzNUNfHjQp9sQl6-xn3NUrP8e7bl-bpCYz3hS-F-Tic
Content-Type: application/json

{
  "name": "Mittens",
  "age": 1,
  "breed": "Persian",
  "image": "https://example.com/mittens.jpg"
}
Ответ:

201 Created - Кошка успешно создана. Возвращается информация о созданной кошке.
json
Copy code
{
  "id": 101,
  "name": "Mittens",
  "age": 1,
  "breed": "Persian",
  "image": "https://example.com/mittens.jpg"
}
400 Bad Request - Ошибка валидации данных.
401 Unauthorized - Неверный токен аутентификации.
Ошибки
Формат ошибок
В случае возникновения ошибки, ответ будет содержать следующую структуру:

json
Copy code
{
  "error": {
    "code": 400,
    "message": "Invalid request",
    "details": [
      {
        "field": "email",
        "message": "Email is required"
      },
      {
        "field": "password",
        "message": "Password is too short"
      }
    ]
  }
}
code - HTTP-код ошибки.
message - сообщение об ошибке.
details - дополнительные детали ошибки, например, недопустимые значения параметров или неверный формат данных.
Теперь вы можете использовать данную документацию для взаимодействия с API интерфейсом проекта KittyGram Backend. Удачи!