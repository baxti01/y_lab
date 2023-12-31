# Запуск проекта
### Создаём .env файл и добавляем следующие настройки

- Настройки сервера
  - `SERVER_HOST=`... (поумолчанию localhost)
  - `SERVER_PORT=`... (поумолчанию 8070)
- Настройки базы данных
  - `POSTGRES_HOST=`... (поумолчанию localhost), установить как (db) для docker
  - `POSTGRES_PORT=`... (поумолчанию 5432)
  - `POSTGRES_DB=`... (обязательное поле)
  - `POSTGRES_USER=`... (обязательное поле)
  - `POSTGRES_PASSWORD=`... (обязательное поле)

### Запускаем проект на компьютере

Устанавливаем зависимости.
```
pip install -r requirements.txt
```

```
python main.py
```

### Запускаем проект в docker.
Но для этого обязательно укажите **POSTGRES_HOST=db**

```
docker-compose up
```

И пользуемся!

---

### Запуск тестов

```
docker-compose -f tests-docker-compose.yml up
```
Или можно запустить в интерактивном режиме
```
docker-compose -f tests-docker-compose.yml up -d
```
---
