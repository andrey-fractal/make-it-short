"""Собирает dist/ из SKILL.md, reference/ и examples/. Запуск: python3 build.py"""
import re, pathlib
R = pathlib.Path(__file__).parent
skill = (R / "SKILL.md").read_text()
stop = (R / "reference/stop-words.md").read_text()
chk = (R / "reference/checklist.md").read_text()
ex = (R / "examples/before-after.md").read_text()

body = re.sub(r"^---\n.*?\n---\n", "", skill, flags=re.S)
start = body.index("### Часть 1. Бокс с правленым текстом")
end = body.index("### Часть 2. Разбор")
plain = """### Часть 1. Правленый текст

Отдай правленый текст в fenced-блоке с языком `text`, чтобы его можно было скопировать одной кнопкой:

````
## Правленый текст
```text
<текст>
```
````

Не выдавай правленый текст голым абзацем: его неудобно копировать. Маркеры `[факт: ___]` остаются как есть.

"""
body = body[:start] + plain + body[end:]
body = body.replace(
    "Ответ состоит из двух частей: **бокс с правленым текстом** (его копируют одной кнопкой) и **разбор** обычным markdown в тексте ответа.",
    "Ответ состоит из двух частей: **правленый текст** в блоке для копирования и **разбор** обычным markdown.")

def strip_h1(s):
    return re.sub(r"^# .*\n", "", s).strip()

full_body = (body
    .replace("Полный список с примерами — в `reference/stop-words.md`.", "Полный список с примерами — в разделе «Справочник: стоп-слова» ниже.")
    .replace("Пройди по `reference/checklist.md`.", "Пройди по разделу «Чек-лист самопроверки» ниже.")
    .replace("## Примеры\nСм. `examples/before-after.md`.", "## Примеры\nСм. раздел «Примеры до/после» ниже."))
full = ("# Системная инструкция: редактор в инфостиле («Пиши, сокращай»)\n\n"
        "Ты — редактор русского текста по методу книги «Пиши, сокращай» (Максим Ильяхов, Людмила Сарычева). "
        "Пользователь присылает текст и, опционально, уровень жёсткости (light / normal / hard) и аудиторию. "
        "Ты возвращаешь правленый текст и разбор. Работай строго по правилам ниже.\n\n"
        + full_body.strip()
        + "\n\n---\n\n# Справочник: стоп-слова\n\n" + strip_h1(stop)
        + "\n\n---\n\n# Чек-лист самопроверки\n\n" + strip_h1(chk)
        + "\n\n---\n\n# Примеры до/после\n\n" + strip_h1(ex) + "\n")

gpt_body = (body
    .replace("Полный список с примерами — в `reference/stop-words.md`.", "Полный список с примерами — в файле stop-words.md.")
    .replace("Пройди по `reference/checklist.md`.", "Пройди по файлу checklist.md.")
    .replace("## Примеры\nСм. `examples/before-after.md`.", "## Примеры\nСм. файл before-after.md."))
gpt = ("Ты — редактор русского текста по методу книги «Пиши, сокращай» (Ильяхов, Сарычева) — инфостиль. "
       "Пользователь присылает текст и, опционально, уровень (light / normal / hard, по умолчанию normal) и аудиторию. "
       "Полный список стоп-слов — в файле stop-words.md, чек-лист — в checklist.md, примеры — в before-after.md: открывай их при каждой правке.\n\n"
       + gpt_body.strip() + "\n")
assert len(gpt) <= 8000, f"chatgpt-instructions.md: {len(gpt)} знаков, лимит 8000"

(R / "dist").mkdir(exist_ok=True)
(R / "dist/system-prompt.md").write_text(full)
(R / "dist/chatgpt-instructions.md").write_text(gpt)
print(f"dist/system-prompt.md: {len(full)} знаков; dist/chatgpt-instructions.md: {len(gpt)} знаков")
