# Подключение MCP сервера к Claude Desktop

## 1. Установка зависимостей

```bash
cd C:\Projects\intervalsicugptcoach
pip install -r requirements.txt
```

## 2. Создание .env файла

Скопируй `.env.example` в `.env` и заполни:

```
ICU_API_KEY=your_api_key_here
ICU_ATHLETE_ID=iXXXXXX
```

Где найти данные:
- **API Key**: intervals.icu → Settings → My Account → API Key
- **Athlete ID**: виден в URL после входа: `https://intervals.icu/athlete/iXXXXXX`

## 3. Конфигурация Claude Desktop

Открой файл конфигурации Claude Desktop:
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

Добавь секцию `mcpServers`:

```json
{
  "mcpServers": {
    "intervals-icu": {
      "command": "python",
      "args": ["C:/Projects/intervalsicugptcoach/mcp_server.py"],
      "env": {
        "ICU_API_KEY": "your_api_key_here",
        "ICU_ATHLETE_ID": "iXXXXXX"
      }
    }
  }
}
```

> Если используешь `.env` файл (рекомендуется), секцию `env` можно убрать.

## 4. Перезапуск Claude Desktop

Полностью закрой и снова открой Claude Desktop. В новом чате должны появиться инструменты intervals.icu.

## 5. Проверка

Напиши в чате:
```
Используй get_athlete_profile и покажи мой текущий FTP и зоны мощности.
```

## 6. Диагностика (если не работает)

```bash
# Проверить что сервер запускается
python C:/Projects/intervalsicugptcoach/mcp_server.py

# Тестирование через MCP Inspector
npx @modelcontextprotocol/inspector python C:/Projects/intervalsicugptcoach/mcp_server.py
```

## Доступные инструменты

| Инструмент | Описание |
|-----------|---------|
| `get_athlete_profile` | Профиль: FTP, зоны, LTHR, вес |
| `list_activities` | Список активностей за период |
| `get_activity` | Детали одной тренировки |
| `get_wellness` | HRV, сон, усталость, форма |
| `get_power_curves` | Кривые мощности (MMP) |
| `get_calendar` | Запланированные тренировки |
| `create_workout` | Создать тренировку в календаре |
| `delete_workout` | Удалить тренировку из календаря |
| `run_weekly_report` | Полный анализ: ACWR, Strain, Monotony, Recovery |
