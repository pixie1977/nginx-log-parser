Сервис, который парсит access-логи nginx и формирует статистический отчет по времени ответа:
- количество запросов;
- минимальное/максимальное время ответа;
- среднее;
- медиана;
- перцентили (P90, P95, P99).

Сервис предоставляет HTTP API (FastAPI) для получения статистики.

## Требования

- Python 3.11+
- nginx, настроенный на вывод access-логов в JSON-формате (см. ниже)
- Docker (опционально, для контейнеризации)

## Формат логов nginx

Рекомендуемый формат (JSON). В `nginx.conf` или include-файле:

```nginx
log_format json_combined escape=json
  '{"time_local":"$time_local",'
   '"remote_addr":"$remote_addr",'
   '"request":"$request",'
   '"status":$status,'
   '"body_bytes_sent":$body_bytes_sent,'
   '"request_time":$request_time,'
   '"upstream_response_time":"$upstream_response_time"}';

access_log /var/log/nginx/access.log json_combined;
```

Сервис ожидает, что каждая строка access-лога — корректный JSON с полями:
- `time_local` (строка, формат `%d/%b/%Y:%H:%M:%S %z`, например `10/Dec/2023:13:55:36 +0000`);
- `remote_addr`;
- `request`;
- `status`;
- `body_bytes_sent`;
- `request_time` (float);
- `upstream_response_time` (строка или `"-"`; опционально).

## Установка для разработки

```bash
git clone https://github.com/your-org/nginx-log-stats-service.git
cd nginx-log-stats-service
make install
```

## Запуск в dev-режиме

По умолчанию путь к логам: `/var/log/nginx/access.log`. Можно переопределить:

```bash
export NGINX_ACCESS_LOG_PATH=/path/to/access.log
export LOG_LEVEL=INFO  # или DEBUG, WARNING и т.д.

make run
```

Сервис будет доступен по адресу: http://localhost:8000

Документация FastAPI (Swagger UI): http://localhost:8000/docs

## Запуск через Docker

Сборка образа:

```bash
docker build -t nginx-log-stats-service .
```

Запуск контейнера, пробрасывая файл логов:

```bash
docker run --rm \
  -e NGINX_ACCESS_LOG_PATH=/logs/access.log \
  -e LOG_LEVEL=INFO \
  -v /var/log/nginx/access.log:/logs/access.log:ro \
  -p 8000:8000 \
  nginx-log-stats-service
```

## Переменные окружения

- `NGINX_ACCESS_LOG_PATH` — путь к файлу access-логов nginx (по умолчанию `/var/log/nginx/access.log`);
- `LOG_LEVEL` — уровень логирования сервиса (`DEBUG`, `INFO`, `WARNING`, ...; по умолчанию `INFO`).

## HTTP API

### GET `/health`

Проверка живости сервиса.

**Ответ 200:**

```json
{
  "status": "ok"
}
```

### GET `/stats/response-time`

Возвращает статистику по времени ответа (`request_time`) по всем строкам лога.

**Успешный ответ 200:**

```json
{
  "count": 12345,
  "min": 0.001,
  "max": 1.234,
  "mean": 0.123,
  "median": 0.110,
  "p90": 0.200,
  "p95": 0.250,
  "p99": 0.400
}
```

**Ошибки:**

- `404` — в логе нет ни одной валидной записи;
- `500` — файл логов не найден или другая ошибка.

## Тесты и качество кода

Запуск линтеров и статического анализа:

```bash
make lint
```

Автоформатирование:

```bash
make format
```

Запуск тестов:

```bash
make test
```

## Структура проекта

- `nginx_log_stats/` — код сервиса;
- `tests/` — тесты и пример лог-файла;
- `.github/workflows/ci.yml` — pipeline CI (GitHub Actions);
- `Dockerfile` — контейнеризация;
- `pyproject.toml` — зависимости и конфигурация инструментов;
- `mypy.ini` — настройки mypy;
- `Makefile` — удобные команды разработчика.
```