## Описание проекта
Этот проект представляет собой API для управления привычками, которое позволяет пользователям добавлять, изменять и удалять свои привычки, а также получать напоминания через Telegram. С помощью API можно отслеживать полезные и приятные привычки, регулировать их частоту и настраивать систему вознаграждений.
## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/DmitriyBorodin/KR7

2. Установите зависимости с помощью Poetry:
    ```bash
    poetry install

3. Настройте переменные окружения.
   Создайте файл .env и добавьте необходимые переменные, такие как:
   ```bash
   SECRET_KEY
   LOCATION
   LOCALHOST
   TELEGRAM_TOKEN
   
   Для подключения базы данных:
   POSTGRES_DB
   POSTGRES_USER
   POSTGRES_PASSWORD
   POSTGRES_HOST
   POSTGRES_PORT

4. Убедитесь, что у вас установлен Docker и Docker Compose.
   Затем выполните:
   ``` bash
   docker-compose up --build
