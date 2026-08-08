# Деплой MCP сервера на VPS для доступа с телефона

Локальный сервер (`mcp_server.py`) работает через stdio — только на том компьютере,
где запущен Claude Desktop. Чтобы пользоваться тренером с телефона, нужен
`mcp_http_server.py`: те же 10 инструментов, но по HTTPS, подключается к claude.ai
как Custom Connector.

Режим **single-tenant**: ключи intervals.icu лежат в `.env` на сервере, сервер
работает с одним атлетом — тобой.

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
