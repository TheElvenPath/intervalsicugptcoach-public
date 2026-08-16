# Деплой MCP сервера на VPS для доступа с телефона

Локальный сервер (`mcp_server.py`) работает через stdio — только на том компьютере,
где запущен Claude Desktop. Чтобы пользоваться тренером с телефона, нужен
`mcp_http_server.py`: те же 10 инструментов, но по HTTPS, подключается к claude.ai
как Custom Connector.

Режим **single-tenant**: ключи intervals.icu лежат в `.env` на сервере, сервер
работает с одним атлетом — тобой.

## Выбери сценарий

**Сценарий А — чистый VPS**, порты 80/443 свободны. Разделы 1–7 ниже: поднимается
свой Caddy, сертификат выпускается автоматически.

**Сценарий Б — на сервере уже есть сайт** за nginx. Отдельный Caddy занять 80/443
не сможет, поэтому MCP встраивается в существующий nginx как location.
См. [«Сценарий Б»](#сценарий-б--рядом-с-существующим-сайтом) в конце файла.

> **Про сервер `155.212.185.155`.** Там же живут сайт и байкфит-портал, и все три
> проекта переезжают на общий Traefik, чтобы деплоиться независимо. Контракт и
> порядок работ — в репозитории `infra`, файл `docs/infra-migration-plan.md`
> (github.com/TheElvenPath/infra). Этой сессии там нужен раздел 3 — контракт —
> и Фаза 2. Копии контракта здесь нет намеренно: он существует в одном месте.

---

## Что понадобится

- VPS с Docker и Docker Compose (подойдёт самый дешёвый — 1 vCPU / 1 GB)
- Домен или поддомен, A-запись которого указывает на IP сервера
- Открытые порты 80 и 443

Порт 80 нужен Let's Encrypt для проверки владения доменом — без него сертификат
не выпустится.

---

## 1. Подготовка домена

Создай A-запись, например `coach.example.com` → IP твоего VPS. Проверь, что она
разошлась:

```bash
dig +short coach.example.com
```

Должен вернуться IP сервера. Если пусто — подожди распространения DNS.

---

## 2. Клонирование на сервер

```bash
git clone https://github.com/TheElvenPath/intervalsicugptcoach-public.git
```

```bash
cd intervalsicugptcoach-public && git checkout mcp-server-v1
```

---

## 3. Генерация секрета

claude.ai не умеет добавлять свои заголовки к запросам, поэтому секрет живёт
в URL: `https://coach.example.com/<MCP_SECRET>/mcp`. Сгенерируй длинный:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Сохрани вывод — он понадобится на шаге 6.

---

## 4. Заполнение .env

```bash
cp .env.example .env && nano .env
```

Заполни четыре переменные:

```
ICU_API_KEY=<ключ из intervals.icu, Settings -> API Key>
ICU_ATHLETE_ID=i116116
MCP_SECRET=<сгенерированное на шаге 3>
MCP_PUBLIC_HOST=coach.example.com
```

`.env` в `.gitignore` — в репозиторий не попадёт. Закрой файл от чужих глаз:

```bash
chmod 600 .env
```

---

## 5. Запуск

```bash
docker compose up -d --build
```

Caddy сам выпустит сертификат Let's Encrypt при первом запросе — это занимает
10–30 секунд. Проверь, что сервер жив:

```bash
curl https://coach.example.com/healthz
```

Ожидаемый ответ: `ok`. Если видишь ошибку сертификата — посмотри логи Caddy:

```bash
docker compose logs caddy --tail 50
```

---

## 6. Подключение к claude.ai

Работает и в браузере, и в мобильном приложении — коннектор привязан к аккаунту,
а не к устройству.

1. Открой [claude.ai](https://claude.ai), раздел **Settings** → **Connectors**
2. Нажми **Add custom connector**
3. Вставь URL целиком, вместе с секретом:
   ```
   https://coach.example.com/<MCP_SECRET>/mcp
   ```
4. Сохрани. В списке инструментов должно появиться 10 штук
   (`run_weekly_report`, `analyze_activity`, `create_workout` и остальные).

---

## 7. Тренерский скилл на claude.ai

Инструменты дают данные, но не методологию. Чтобы получить того же тренера, что
в Claude Code:

1. Создай Project на claude.ai
2. В **Project instructions** вставь содержимое
   [.claude/commands/cycling-coach/SKILL.md](.claude/commands/cycling-coach/SKILL.md)
3. Референсы (`references/methodology.md`, `report-format.md`,
   `workout-format.md`) загрузи в **Project knowledge**

Дальше в любом чате внутри проекта — «проанализируй мои тренировки», и тренер
подтянет живые данные через коннектор.

---

## Обновление после изменений в коде

```bash
git pull && docker compose up -d --build
```

---

## Безопасность

Что защищает сервер:

| Механизм | От чего |
|---|---|
| Секрет в URL (>=24 символа) | Случайное обнаружение сканерами |
| Проверка заголовка `Host` | DNS-rebinding атаки |
| Allow-list `Origin` | Запросы с чужих сайтов через браузер жертвы |
| URI вырезан из логов Caddy | Утечка секрета через access.log |
| `--no-access-log` у uvicorn | То же самое на уровне приложения |
| Непривилегированный пользователь в контейнере | Эскалация при компрометации |

Чего этот вариант **не** даёт: секрет статичный и не истекает. Любой, кто
получил полный URL, имеет полный доступ к календарю intervals.icu — включая
запись и удаление тренировок. Поэтому:

- не вставляй URL в скриншоты, чаты и issue-трекеры
- при подозрении на утечку смени `MCP_SECRET` в `.env` и перезапусти
  (`docker compose up -d`), затем обнови URL коннектора в claude.ai
- для нескольких атлетов такой схемы недостаточно — там нужен OAuth и
  рефакторинг `intervals_icu_adapter.py`, который сейчас держит ключи
  в глобальных переменных модуля

---

## Диагностика

**Коннектор не подключается.** Проверь `curl https://coach.example.com/healthz`.
Если `ok` — проблема в URL коннектора: скорее всего потерян `/mcp` в конце или
неверный секрет.

**HTTP 421 Invalid Host header.** `MCP_PUBLIC_HOST` в `.env` не совпадает
с доменом, по которому идёт запрос.

**HTTP 403 Invalid Origin header.** Клиент прислал origin, которого нет в
allow-list. Добавь его в `MCP_ALLOWED_ORIGINS` через запятую и перезапусти.

**Инструменты видны, но возвращают ошибку.** Почти всегда неверные
`ICU_API_KEY` / `ICU_ATHLETE_ID`. Проверь логи приложения:

```bash
docker compose logs mcp --tail 50
```

---

# Сценарий Б — рядом с существующим сайтом

Когда порты 80/443 уже держит nginx сайта, MCP публикуется как путь на том же
домене: `https://<домен>/icu/<MCP_SECRET>/mcp`. Отдельный домен, DNS-запись и
второй сертификат не нужны, сайт не останавливается.

MCP при этом живёт **отдельным compose-проектом** и в свою сеть публикует только
внутренний порт. Деплой сайта (`docker compose up -d --build` в его каталоге)
чужие проекты не трогает, а `docker image prune -f` удаляет только висячие
образы — так что редеплой сайта MCP не уронит, и наоборот.

## Б1. Конфиг nginx кладётся в репозиторий САЙТА

Это главное. Каталог сайта на сервере — рабочая копия git, и деплой делает
`git pull`. Правка `locations.conf` руками на сервере либо будет затёрта, либо
уронит деплой конфликтом. Поэтому содержимое
[deploy/nginx-mcp-location.conf](deploy/nginx-mcp-location.conf) добавляется
в репозиторий сайта — в тот файл, который уже подключён внутри `server`-блока
443 (для doc-skibavv.ru это `nginx/conf.d/locations.conf`).

Секрета в этом сниппете нет — он проксирует префикс `/icu/`, а секрет проверяет
уже само приложение. Файл безопасно коммитить.

После пуша в репозиторий сайта автодеплой сам разложит конфиг и перезапустит nginx.

## Б2. Разворачивание MCP

На сервере, в отдельном каталоге (не внутри каталога сайта):

```bash
git clone https://github.com/TheElvenPath/intervalsicugptcoach-public.git /opt/intervals-mcp
```

```bash
cd /opt/intervals-mcp && git checkout mcp-server-v1 && cp .env.example .env && chmod 600 .env
```

Заполни `.env`. Важное отличие от сценария А: `MCP_PUBLIC_HOST` — это домен
**сайта**, потому что именно его nginx передаёт в заголовке `Host`.

```
ICU_API_KEY=<ключ intervals.icu>
ICU_ATHLETE_ID=i116116
MCP_SECRET=<python3 -c "import secrets; print(secrets.token_urlsafe(32))">
MCP_PUBLIC_HOST=doc-skibavv.ru
MCP_PROXY_NETWORK=vskiba_web
```

`MCP_PROXY_NETWORK` — docker-сеть, в которой работает nginx сайта. Посмотреть:

```bash
docker inspect <имя-контейнера-nginx> --format '{{range $k,$v := .NetworkSettings.Networks}}{{$k}}{{end}}'
```

Запуск:

```bash
cd /opt/intervals-mcp && docker compose -f docker-compose.nginx.yml up -d --build
```

Проверка изнутри сети, до того как endpoint станет публичным:

```bash
docker exec <имя-контейнера-nginx> wget -qO- http://mcp-intervals:8000/healthz
```

Должно вернуть `ok`.

## Б3. Подключение к claude.ai

URL коннектора: `https://doc-skibavv.ru/icu/<MCP_SECRET>/mcp`

Дальше как в разделе 6 сценария А.

## Б4. Обновление MCP

Автоматически: пуш в ветку `mcp-server-v1` запускает
[.github/workflows/deploy.yml](.github/workflows/deploy.yml). Изменения только
в `*.md` и `docs/` деплой не вызывают.

Workflow состоит из двух шагов, и первый важнее второго:

1. **`smoke`** — собирает образ и **запускает** его с фиктивными ключами, проверяя
   `/healthz`, регистрацию всех десяти инструментов и то, что чужой `Origin`
   по-прежнему отклоняется. Успешная сборка ничего не доказывает: незакреплённый
   `mcp>=1.26.0` однажды разрешился в 2.0.0 с переименованным
   `mcp.server.fastmcp` — образ собрался и умер при импорте. Ловится только
   запуском.
2. **`deploy`** — идёт по SSH, `reset --hard` на ветку, пересобирает контейнер,
   ждёт статус `healthy` и отдельно проверяет, что endpoint отвечает **через
   Traefik**. Маршрутизация и TLS живут в репозитории `infra` и могут сломаться
   без единой правки здесь.

Нужны секреты репозитория: `SSH_HOST`, `SSH_USER`, `SSH_PRIVATE_KEY`.

`reset --hard` не трогает файлы вне git, поэтому `.env` переживает деплой —
секрет и URL коннектора остаются прежними, перенастраивать claude.ai не нужно.

Репозиторий публичный, значит логи Actions тоже публичные: скрипт деплоя
проверяет живой endpoint, ни разу не печатая секрет и URL с ним.

Вручную, если нужно:

```bash
cd /opt/intervals-mcp && git pull && docker compose -f docker-compose.traefik.yml up -d --build
```

Локальный прогон smoke-теста перед пушем:

```bash
docker build -t intervals-mcp:local . && ./scripts/smoke-test.sh intervals-mcp:local
```

## Почему конфиг устроен именно так

**`resolver` вместо обычного имени апстрима.** Если написать
`proxy_pass http://mcp-intervals:8000` напрямую, nginx резолвит имя при старте и
**отказывается запускаться**, когда контейнер недоступен — то есть остановленный
MCP утащил бы за собой весь сайт. Проверено: с литеральным именем nginx падает
с `host not found in upstream`. Через `resolver` + переменную имя разрешается
на каждый запрос, и лежащий MCP даёт 502 только на `/icu/`.

**`access_log off`.** Секрет лежит в пути запроса, а nginx сайта пишет access-лог
в stdout контейнера. Без этой строки секрет попадал бы в `docker logs`.

**`proxy_buffering off`.** MCP отдаёт результаты через SSE. С буферизацией
события копились бы до конца ответа, и длинный отчёт выглядел бы как зависание.

**`proxy_read_timeout 300s`.** `run_weekly_report` делает несколько
последовательных запросов к intervals.icu; дефолтных 60 секунд может не хватить.

## Что проверено

Вся цепочка прогнана локально на копии структуры сайта — nginx с тем же
`locations.conf` плюс контейнер MCP в общей docker-сети:

| Проверка | Результат |
|---|---|
| `tools/list` через `/icu/<секрет>/mcp` | 10 инструментов |
| Реальный `get_athlete_profile` | вернул данные из intervals.icu |
| Неверный секрет | 404 |
| `Origin: https://doc-skibavv.ru` (origin сайта) | 403 — отклонён |
| Путь `/` сайта | 200, не задет |
| Секрет в логах nginx | отсутствует |
| MCP остановлен: сайт | 200 |
| MCP остановлен: `/icu/` | 502 |
| Рестарт nginx при лежащем MCP | стартует, сайт 200 |
