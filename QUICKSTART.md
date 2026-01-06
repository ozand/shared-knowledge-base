# Knowledge Base - Quick Start

**5 минут до полной настройки**

## 1. Установка (30 секунд)

```bash
# Убедитесь, что установлен Python 3.8+
python --version

# Установите зависимости
pip install pyyaml
# ИЛИ для этого проекта:
uv add pyyaml --optional dev
```

## 2. Первый запуск (1 минута)

```bash
# Перейдите в корень проекта
cd /path/to/your/project

# Постройте индекс базы знаний
python docs/knowledge-base/tools/kb.py index -v

# Вывод:
# 📚 Building index from: docs/knowledge-base
#   ✓ Indexed: IMPORT-001 - Circular Import Between ETL Modules
#   ✓ Indexed: TYPE-001 - Mypy Too Strict for Test Files
#   ...
# ✓ Indexed 15 entries
```

## 3. Первый поиск (10 секунд)

```bash
# Поиск по ключевому слову
python docs/knowledge-base/tools/kb.py search "async test"

# Результат:
# 📚 Found 2 result(s):
#
# 1. 🟠 TEST-001: Async Test Without @pytest.mark.asyncio
#    Category: testing | Severity: high | Scope: python
#    Tags: async, pytest, decorator
#    File: docs/knowledge-base/errors/testing.yaml
```

## 4. Создание алиаса (опционально, 30 секунд)

### Windows (PowerShell)

```powershell
# Добавьте в профиль PowerShell
notepad $PROFILE

# Добавьте строку:
function kb { python docs/knowledge-base/tools/kb.py $args }

# Перезапустите PowerShell, теперь можно:
kb search "import error"
kb stats
```

### macOS / Linux / Git Bash

```bash
# Добавьте в ~/.bashrc или ~/.zshrc
echo 'alias kb="python docs/knowledge-base/tools/kb.py"' >> ~/.bashrc

# Перезагрузите shell
source ~/.bashrc

# Теперь можно:
kb search "import error"
kb stats
```

### Или создайте символическую ссылку (Unix/Mac)

```bash
chmod +x docs/knowledge-base/tools/kb.py
sudo ln -s "$(pwd)/docs/knowledge-base/tools/kb.py" /usr/local/bin/kb

# Теперь kb доступен глобально:
kb search "anything"
```

## 5. Статистика (5 секунд)

```bash
kb stats

# 📊 Knowledge Base Statistics
#
# Total entries: 15
#
# By Category:
#   testing: 6
#   imports: 4
#   types: 3
#   ...
```

---

## Частые команды

```bash
# Поиск
kb search "keyword"                    # Простой поиск
kb search --category testing           # По категории
kb search --severity high              # По серьезности
kb search --tags async pytest          # По тегам

# Управление
kb index                               # Перестроить индекс
kb index -v                            # Verbose режим
kb stats                               # Статистика

# Валидация
kb validate path/to/file.yaml         # Проверить файл

# Экспорт
kb export --format json               # Экспорт в JSON
kb export --output kb.json            # Экспорт в файл
```

---

## Использование в AI инструментах

### Claude Code

```markdown
В начале сессии спросите Claude:

"Search the knowledge base for async testing errors"

Claude выполнит:
kb search "async test"
```

### GitHub Copilot / Cursor

```bash
# Экспортируйте KB в JSON
kb export --format json --output .kb-snapshot.json

# AI инструменты могут использовать JSON для контекста
```

---

## Добавление новой ошибки (2 минуты)

1. **Создайте файл:**

```bash
# Если категория уже существует
vim docs/knowledge-base/errors/existing-category.yaml

# Если новая категория
vim docs/knowledge-base/errors/new-category.yaml
```

2. **Используйте шаблон:**

```yaml
version: "1.0"
category: "category-name"
last_updated: "2026-01-04"

errors:
  - id: "CATEGORY-001"
    title: "Error Description"
    severity: "high"
    scope: "python"

    problem: |
      What went wrong

    symptoms:
      - "Error message"

    wrong_code: |
      # Wrong code

    correct_code: |
      # Correct code

    prevention:
      - "How to avoid"

    tags: ["tag1", "tag2"]
```

3. **Валидация и индексация:**

```bash
kb validate docs/knowledge-base/errors/new-category.yaml
kb index
```

4. **Коммит:**

```bash
git add docs/knowledge-base/errors/new-category.yaml
git commit -m "kb: Add CATEGORY-001 error"
```

---

## Синхронизация с Shared KB (опционально)

**🌟 РЕКОМЕНДАЦИЯ (v3.1):** Используйте **git submodule + sparse checkout** для интеграции Shared KB

**Новое в v3.1:** Sparse checkout исключает Curator файлы, загружая только контент для Project Agents!

### Вариант 1: Автоматический setup с Sparse Checkout (РЕКОМЕНДУЕТСЯ ✅)

**Linux/Mac:**
```bash
cd /path/to/your/project
bash /path/to/shared-knowledge-base/scripts/setup-shared-kb-sparse.sh
```

**Windows (PowerShell):**
```powershell
cd C:\path\to\your\project
powershell -ExecutionPolicy Bypass -File \
  C:\path\to\shared-knowledge-base\scripts\setup-shared-kb-sparse.ps1
```

**Что делает скрипт:**
- ✅ Добавляет submodule с sparse checkout
- ✅ Загружает только паттерны + agent guides
- ✅ Исключает curator/, *_ANALYSIS.md, *_REPORT.md
- ✅ Экономия ~22% размера + чистый контекст

### Вариант 2: Стандартный Submodule

```bash
# Добавить как submodule
git submodule add https://github.com/ozand/shared-knowledge-base.git \
  docs/knowledge-base/shared

# Скопировать kb.py tool (однократно)
cp docs/knowledge-base/shared/tools/kb.py docs/knowledge-base/tools/

# Обновить индекс
kb index -v

# Теперь поиск включает и shared KB
kb search "async"  # Найдет и локальные, и shared записи

# Обновление shared KB (когда выходит новая версия)
git submodule update --remote --merge docs/knowledge-base/shared
kb index -v
```

**Проверка обновлений:**
```bash
# Автоматическая проверка при старте агента
python docs/knowledge-base/shared/tools/kb-agent-bootstrap.py

# Или вручную
python docs/knowledge-base/shared/tools/kb.py check-updates
```

### Вариант 3: Clone (только для тестов/экспериментов)

```bash
# Простой clone (только для quick start/тестов)
git clone https://github.com/ozand/shared-knowledge-base.git \
  docs/knowledge-base/shared

# Обновление (вручную)
cd docs/knowledge-base/shared
git pull
cd ../..
kb index -v
```

**📖 Документация:**
- **[SUBMODULE_VS_CLONE.md](SUBMODULE_VS_CLONE.md)** - Детальное сравнение подходов
- **[SUBMODULE_CONTEXT_CONTAMINATION_ANALYSIS.md](SUBMODULE_CONTEXT_CONTAMINATION_ANALYSIS.md)** - Почему sparse checkout важен
- **[scripts/README.md](scripts/README.md)** - Документация setup скриптов

---

## Troubleshooting

### "kb not found"

```bash
# Используйте полный путь
python docs/knowledge-base/tools/kb.py search "..."

# Или создайте алиас (см. выше)
```

### "No results found"

```bash
# Проверьте, построен ли индекс
kb stats

# Если total = 0, постройте индекс
kb index -v
```

### "YAML error"

```bash
# Проверьте файл
kb validate docs/knowledge-base/errors/file.yaml

# Исправьте ошибки и перестройте
kb index -v
```

---

## Следующие шаги

1. ✅ **Настроили** - Индекс построен, алиас создан
2. 📖 **Читайте** - [HYBRID_APPROACH.md](HYBRID_APPROACH.md) для деталей
3. 🔍 **Используйте** - `kb search` каждый раз при ошибке
4. 📝 **Документируйте** - Добавляйте новые ошибки по мере решения
5. 🤝 **Делитесь** - Contribute в shared repository

---

**Готово! Теперь база знаний работает. 🎉**

Вопросы? См. [HYBRID_APPROACH.md](HYBRID_APPROACH.md) для полной документации.
