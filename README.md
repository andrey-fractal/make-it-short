# make-it-short — скилл «Пиши, сокращай» для LLM

Редактор русского текста в инфостиле по методу книги **«Пиши, сокращай»** (Максим Ильяхов, Людмила Сарычева). Убирает стоп-слова, канцелярит, штампы и воду, переписывает в мире читателя, показывает разбор каждой правки.

Работает как [Agent Skill](https://agentskills.io) (формат `SKILL.md`) в Claude Code, Claude Desktop, Codex, Cursor, Copilot и других агентах, а также как системный промпт в ChatGPT, Gemini и любом чате.

**Теги:** инфостиль, Ильяхов, редактура, сокращение текста, канцелярит, стоп-слова, деловая переписка · *Russian infostyle editor, text tightening, copywriting skill for Claude / ChatGPT / Gemini*

---

## Что делает

Вход: текст и уровень жёсткости.

| Уровень | Что делает |
|---|---|
| `light` | Убирает только мусор: стоп-слова, канцелярит. Голос и структуру не трогает |
| `normal` | + переписывает слабый синтаксис, правит абзацы и заголовки. Тон автора сохраняет (по умолчанию) |
| `hard` | «Как Ильяхов»: режет всё, что можно, перестраивает структуру, добавляет конкретику. Текст может ужаться в 2–3 раза |

Выход: правленый текст в блоке с кнопкой копирования и разбор — какие стоп-слова найдены, что переписано в синтаксисе и структуре, каких фактов не хватает (`[факт: ___]`).

### Пример

Было:

> К сожалению, вынужден вам сообщить, что мы не уверены, что сможем поставить товар в надлежащий срок. Уверен, что вы пойдете нам навстречу и окажете содействие.

Стало (`hard`):

> Мы не успеваем поставить [товар] к [срок по договору]. Сможем отгрузить [новая дата].
>
> Подтвердите, пожалуйста, что новый срок подходит. Если нет — напишите, и мы предложим [варианты].

Разбор: «к сожалению, вынужден сообщить» — вводная связка, убрано; «не уверены, что сможем» — эвфемизм; «надлежащий срок» — канцелярит без факта; «пойдёте навстречу и окажете содействие» — непонятно, что просите.

---

## Установка

### Claude Code

Глобально, для всех проектов:

```bash
git clone https://github.com/andrey-fractal/make-it-short ~/.claude/skills/make-it-short
```

Только в текущий проект:

```bash
git clone https://github.com/andrey-fractal/make-it-short .claude/skills/make-it-short
```

Или через [skills CLI](https://skills.sh):

```bash
npx skills add andrey-fractal/make-it-short
```

Вызов: `/make-it-short hard <текст>` или просто «сократи этот текст» — Claude подхватит скилл сам.

### Claude Desktop и claude.ai

1. Скачайте `make-it-short.zip` из [Releases](https://github.com/andrey-fractal/make-it-short/releases).
2. Настройки → Возможности (Capabilities) → Skills → Загрузить.
3. В чате: «Сократи по инфостилю, уровень hard: …».

### OpenAI Codex

Codex читает тот же формат `SKILL.md`:

```bash
git clone https://github.com/andrey-fractal/make-it-short ~/.codex/skills/make-it-short
```

### Cursor

```bash
git clone https://github.com/andrey-fractal/make-it-short .cursor/skills/make-it-short
```

### GitHub Copilot (VS Code, CLI)

```bash
git clone https://github.com/andrey-fractal/make-it-short .github/skills/make-it-short
```

### Gemini CLI

Если ваша версия поддерживает Agent Skills (`gemini skills list`):

```bash
git clone https://github.com/andrey-fractal/make-it-short ~/.gemini/skills/make-it-short
```

Если нет — добавьте содержимое [`dist/system-prompt.md`](dist/system-prompt.md) в `GEMINI.md` проекта.

### ChatGPT

**Custom GPT:** в поле Instructions вставьте [`dist/chatgpt-instructions.md`](dist/chatgpt-instructions.md), в Knowledge загрузите `reference/stop-words.md`, `reference/checklist.md`, `examples/before-after.md`.

**Project:** в инструкции проекта вставьте [`dist/system-prompt.md`](dist/system-prompt.md) целиком.

### Gemini Gems, Mistral, DeepSeek, локальные модели

Используйте [`dist/system-prompt.md`](dist/system-prompt.md) как системный промпт. Это весь скилл в одном файле: правила, стоп-слова, чек-лист и примеры.

---

## Структура

```
SKILL.md                  — инструкция для агента (формат Agent Skills)
reference/stop-words.md   — 11 категорий стоп-слов с примерами замен
reference/checklist.md    — чек-лист самопроверки
examples/before-after.md  — примеры правок на трёх уровнях
dist/system-prompt.md     — всё в одном файле для чатов без поддержки скиллов
dist/chatgpt-instructions.md — короткая версия для Custom GPT (лимит 8000 знаков)
```

`dist/` собирается из исходников: `python3 build.py`.

---

## English

**make-it-short** is an Agent Skill that edits Russian text in the "infostyle" of the book *Pishi, sokrashchay* ("Write, Cut") by Maxim Ilyakhov and Lyudmila Sarycheva: removes filler and bureaucratese, rewrites for the reader, and explains every change. Three strictness levels (`light` / `normal` / `hard`). Install into Claude Code, Codex, Cursor or Copilot by cloning into the skills folder (see above), or use `dist/system-prompt.md` as a system prompt in ChatGPT, Gemini or any other model.

## Лицензия

MIT. Метод и терминология — из книги «Пиши, сокращай»; это неофициальный инструмент, не связанный с авторами книги.
