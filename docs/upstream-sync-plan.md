# План синхронизации с апстримом

Составлен 16.08.2026. Правило заказчика: **берём то, что лучше нашего; не берём
то, что такое же или хуже.**

## Откуда синхронизируемся

Не из `origin/main` — он заморожен на 30.03.2026 и отстаёт даже от наших
апрельских синков. Общего предка у `mcp-server-v1` с ним нет: ветка заводилась
отдельной историей, синхронизация делалась копированием файлов.

Настоящий источник — `revo2wheels/main`, подключён в `_upstream`:

```bash
git -C _upstream fetch revo2wheels
```

С нашего последнего синка (`387baf6`, 28.04.2026, база апстрима `6fb7bf7`) там
**202 коммита**. Ченджлог — не `docs/CHANGELOG.md` (он заглушка), а закрытые
issues `#47`–`#60`, релизы 5.4.106–5.4.113.

## Что мы правили — это нужно сохранить

Реальные расхождения невелики. Числа посчитаны с игнорированием CRLF: без этого
`report_controller.py` показывает 2151 строку разницы, хотя правок там 7.

| Файл | Строк | Что это |
|---|---|---|
| `semantic_json_builder.py` | 76 | **Критично.** Нормализация формы `sportSettings` (list или dict) и защита `types`. Нужно потому, что прямой API intervals.icu отдаёт не то же, что Cloudflare-воркер апстрима |
| `coaching_cheat_sheet.py` | 12 | Отдельная спорт-группа `Hike` |
| `audit_core/report_controller.py` | 7 | `CURRENT_DIR` в `sys.path` (иначе не резолвятся bare-импорты новых модулей) + `print` → `stderr` |
| `audit_core/tier3_espe.py` | 13 | Багфикс 5.4.113, уже совпадает с апстримом |
| `questions_engine.py` | 2 | Тот же багфикс, уже совпадает |

Файлы, которых у апстрима нет вообще и которые синк не касается:
`mcp_server.py`, `mcp_http_server.py`, `intervals_client.py`,
`intervals_icu_adapter.py`, `reports.py`, `audit_core/tier2_activity_streams.py`.

## Про DFA-alpha1: конкурента нет

Релиз 5.4.113 заявляет «AlphaHRV support for MCP and API». Проверено: **в
открытом коде апстрима нет ни одного упоминания alpha** ни в одном `.py`.
`docs/alphahrvguide.md` описывает, как Garmin AlphaHRV кладёт данные в кастомные
поля intervals.icu, а читает их их хостинговый сервис Montis.

Значит наш `tier2_activity_streams.py` сравнивать не с чем. **Оставляем свой,
брать нечего.**

## Что берём

Во всех этих файлах наша копия идентична базе апстрима, то есть своей работы там
нет и терять нечего — чистое обновление.

| Модуль | Объём | Что нового |
|---|---|---|
| `audit_core/tier1_controller.py` | +823 | `safe_stats`, `safe_z`, `resolve_metric_chain` — устойчивость к пропускам данных |
| `audit_core/tier2_actions.py` | +372 | `classify_phase_v2`, `build_future_projected_weeks`, затухание CTL/ATL к концу недели |
| `audit_core/tier3_adaptive_decision_engine.py` | +411 | Учёт контекста целевого события, скоринг решений со штрафами и поддержкой |
| `audit_core/tier3_performance_intelligence.py` | +147 | `_completed_wellness_days` |
| `audit_core/tier2_derived_metrics.py` | +78 | правки метрик |
| `coaching_profile.py` | +498 | наполнение профиля, новых функций нет |
| `prompt_builder.py` | — | обновление |
| `audit_core/event_readiness.py` | новый | готовность к событию; подключён к ADE и semantic builder |

С переносом наших правок поверх:

| Модуль | Объём | Что нового |
|---|---|---|
| `semantic_json_builder.py` | +1552 | `resolve_training_load_pattern`, `resolve_physiology_state`, `apply_report_recency_governance`, `classify_race_type` |
| `coaching_cheat_sheet.py` | +385 | наполнение |
| `audit_core/report_controller.py` | — | обновление |

## Что НЕ берём

| Файл | Почему |
|---|---|
| `app.py` | Flask/Railway — их хостинг, у нас MCP |
| `report.py` (+1161) | CLI-обвязка, дублирует нашу роль |
| `i18n/` | Перевод для их приложения; наш клиент — Claude, он переводит сам |
| `OPENAI/`, `instructionsv17.md` | Промпты для ChatGPT |
| `public/`, `assets/` | Иконки PWA и картинки гайдов |
| `docs/CHANGELOG.md` | Заглушка |

## Порядок и риски

**Движок берётся целиком, а не по частям.** `semantic_json_builder` вырос на 1552
строки и рассчитывает на ключи контекста, которые производят обновлённые
`tier1_controller` и `tier2_actions`. Частичный синк даст рассогласование, причём
тихое: отчёт соберётся, но поля будут пустыми.

Порядок:

1. Ветка `sync-2026-08` от `mcp-server-v1`.
2. Снять наши патчи в отдельные файлы (`git diff` против базы апстрима) — по
   таблице выше их пять, суммарно ~110 строк.
3. Скопировать модули из списка «берём».
4. Наложить патчи обратно. Самый рискованный — `semantic_json_builder.py`:
   функция вокруг `sportSettings` могла быть переписана, тогда нормализацию
   придётся встраивать заново, а не применять патчем.
5. Прогнать проверки.

**Что проверять:**

- `intervals_icu_adapter.py` патчит `tier0_pre_audit.fetch_with_retry` и
  `tier3_future_forecast.fetch_calendar_fallback`. Оба файла апстрим **не менял**
  — риск низкий, но сигнатуры сверить.
- `run_weekly_report` на живых данных: строится ли отчёт, не опустели ли секции.
- `analyze_activity` с потоками: наш `tier2_activity_streams` не должен
  пострадать.
- Новые модули могут тянуть импорты, которых у нас нет.
- Smoke-тест и деплой прогонят это автоматически при пуше.

**Откат** — ветка не мержится, пока `run_weekly_report` не даст осмысленный
отчёт на реальных данных.
