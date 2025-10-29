"""
Скрипт для автоматической генерации документации проекта.

Использует pdoc для создания HTML документации из docstrings.
"""

import subprocess
import os
import webbrowser
import sys
from pathlib import Path


def check_pdoc_installation():
    """Проверяет установлен ли pdoc."""
    try:
        subprocess.run([sys.executable, "-m", "pdoc", "--version"],
                       capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def install_pdoc():
    """Устанавливает pdoc если не установлен."""
    print("📦 Установка pdoc...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pdoc"],
                       check=True)
        print("✅ pdoc успешно установлен")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка установки pdoc: {e}")
        return False


def generate_html_docs():
    """Генерирует HTML документацию."""
    print("🎨 Генерация HTML документации...")

    # Создаем папку для документации
    docs_dir = "html_docs"
    os.makedirs(docs_dir, exist_ok=True)

    # Файлы для документирования
    files_to_document = ["book.py", "reader.py", "library.py", "main.py"]

    # Проверяем существование файлов
    existing_files = [f for f in files_to_document if os.path.exists(f)]

    if not existing_files:
        print("❌ Не найдены файлы для документирования")
        return False

    try:
        # Генерируем документацию
        cmd = [sys.executable, "-m", "pdoc", "-o", docs_dir] + existing_files
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        print("✅ HTML документация успешно сгенерирована!")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка генерации документации: {e}")
        print(f"Stderr: {e.stderr}")
        return False


def generate_web_server():
    """Запускает веб-сервер для просмотра документации."""
    print("🌐 Запуск веб-сервера для документации...")

    try:
        # Запускаем pdoc в режиме веб-сервера
        cmd = [sys.executable, "-m", "pdoc", "-p", "8080", "book.py", "reader.py", "library.py", "main.py"]
        print("📖 Документация доступна по адресу: http://localhost:8080")
        print("🛑 Для остановки сервера нажмите Ctrl+C")

        subprocess.run(cmd)

    except KeyboardInterrupt:
        print("\n⏹️ Сервер остановлен")
    except Exception as e:
        print(f"❌ Ошибка запуска сервера: {e}")


def create_markdown_docs():
    """Создает Markdown документацию."""
    print("📝 Генерация Markdown документации...")

    md_docs_dir = "markdown_docs"
    os.makedirs(md_docs_dir, exist_ok=True)

    files_to_document = ["book.py", "reader.py", "library.py", "main.py"]

    try:
        for file in files_to_document:
            if os.path.exists(file):
                module_name = file.replace('.py', '')
                output_file = os.path.join(md_docs_dir, f"{module_name}.md")

                cmd = [sys.executable, "-m", "pdoc", "--format", "markdown", file]
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)

                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(result.stdout)

                print(f"✅ {file} -> {output_file}")

        print("📁 Markdown документация сохранена в папке 'markdown_docs'")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка генерации Markdown: {e}")
        return False


def open_html_docs():
    """Открывает HTML документацию в браузере."""
    index_path = os.path.abspath("html_docs/index.html")

    if os.path.exists(index_path):
        print(f"📄 Открываю документацию в браузере...")
        webbrowser.open(f"file://{index_path}")
    else:
        # Ищем первый доступный HTML файл
        for file in os.listdir("html_docs"):
            if file.endswith(".html"):
                file_path = os.path.abspath(f"html_docs/{file}")
                webbrowser.open(f"file://{file_path}")
                break


def main():
    """Основная функция генерации документации."""
    print("=" * 60)
    print("📚 ГЕНЕРАТОР ДОКУМЕНТАЦИИ ДЛЯ БИБЛИОТЕЧНОЙ СИСТЕМЫ")
    print("=" * 60)

    # Проверяем установку pdoc
    if not check_pdoc_installation():
        print("❌ pdoc не установлен")
        if not install_pdoc():
            return

    print("\n1. 🎨 Генерация HTML документации...")
    if generate_html_docs():
        open_html_docs()

    print("\n2. 📝 Генерация Markdown документации...")
    create_markdown_docs()

    print("\n3. 🌐 Запуск интерактивной документации...")
    print("   Хочешь запустить веб-сервер для документации? (y/n)")

    if input().lower() == 'y':
        generate_web_server()

    print("\n" + "=" * 60)
    print("✅ ДОКУМЕНТАЦИЯ УСПЕШНО СГЕНЕРИРОВАНА!")
    print("=" * 60)
    print("\n📁 Структура документации:")
    print("   ├── html_docs/     - HTML версия документации")
    print("   ├── markdown_docs/ - Markdown версия документации")
    print("   └── http://localhost:8080 - Интерактивная версия")


if __name__ == "__main__":
    main()