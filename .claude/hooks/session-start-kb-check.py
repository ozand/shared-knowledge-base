#!/usr/bin/env python
"""
SessionStart Hook: Проверка обновлений Shared Knowledge Base

Запускается при старте каждой сессии:
- Проверяет наличие обновлений
- Предлагает обновить если доступно
- НЕ обновляет автоматически (только предложение)
"""

import subprocess
import sys
from pathlib import Path

def check_kb_updates():
    """Проверяет наличие обновлений Shared KB"""

    # Проверяем, находимся ли мы в проекте с KB
    kb_path = Path('.kb/shared')
    if not kb_path.exists():
        return  # KB не установлен, ничего не делаем

    # Проверяем, что это действительно submodule
    gitmodules = Path('.gitmodules')
    if not gitmodules.exists():
        return

    try:
        content = gitmodules.read_text(encoding='utf-8')
        if 'shared-knowledge-base' not in content:
            return  # Не наш KB
    except Exception:
        return

    # Проверяем статус submodule
    try:
        # Fetch для проверки (async, с timeout)
        result = subprocess.run(
            ['git', '-C', str(kb_path), 'fetch', 'origin'],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            return  # Ошибка network/git, игнорируем

        # Сравниваем версии
        result = subprocess.run(
            ['git', '-C', str(kb_path), 'log', 'HEAD..origin/main', '--oneline'],
            capture_output=True,
            text=True,
            timeout=10
        )

        new_commits = result.stdout.strip()

        if new_commits:
            # Есть обновления!
            print("\n" + "=" * 60)
            print("📦 Доступны обновления Shared Knowledge Base")
            print("=" * 60)

            # Показываем последние 3-5 commits
            commits = new_commits.split('\n')[:5]
            for i, commit in enumerate(commits, 1):
                print(f"  {i}. {commit}")

            print("\nДля обновления выполните:")
            print("  /kb-update")
            print("  или:")
            print("  git submodule update --remote .kb/shared")
            print("=" * 60 + "\n")

    except subprocess.TimeoutExpired:
        # Timeout - игнорируем, не замедляем старт сессии
        return
    except Exception:
        # Любая ошибка - игнорируем, не ломаем сессию
        return

if __name__ == '__main__':
    check_kb_updates()
