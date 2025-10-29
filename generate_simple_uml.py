import subprocess
import os
import sys


def generate_uml_with_pyreverse():
    """Генерирует UML диаграмму с помощью pyreverse (встроен в pylint)"""

    print("🎨 Генерация UML диаграмм с помощью pyreverse...")

    # Команды для генерации разных типов диаграмм
    commands = [
        # Диаграмма классов
        ['pyreverse', '-o', 'png', '-p', 'LibrarySystem', 'book.py', 'reader.py', 'library.py', 'main_window.py'],
        # Диаграмма пакетов
        ['pyreverse', '-o', 'png', '-p', 'Packages', '-k', 'book.py', 'reader.py', 'library.py', 'main_window.py']
    ]

    for cmd in commands:
        try:
            print(f"Выполняется: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print("✅ Диаграмма успешно создана!")
            else:
                print(f"⚠️  Предупреждение: {result.stderr}")

        except Exception as e:
            print(f"❌ Ошибка: {e}")

    # Проверяем какие файлы создались
    created_files = [f for f in os.listdir('.') if f.startswith('classes_') or f.startswith('packages_')]
    print(f"\n📁 Созданные файлы: {created_files}")


def create_text_uml():
    """Создает текстовое представление UML диаграммы"""

    print("\n📝 Текстовое представление UML диаграммы:")
    print("=" * 50)

    uml_text = """
    ╔══════════════════════════════════════════╗
    ║             UML Class Diagram            ║
    ╚══════════════════════════════════════════╝

    📚 Book
    ├── Атрибуты:
    │   ├── title: str
    │   ├── author: str
    │   ├── isbn: str
    │   ├── year: int
    │   └── is_available: bool
    ├── Методы:
    │   ├── __init__(title, author, isbn, year)
    │   ├── to_dict()
    │   ├── from_dict(data)
    │   └── __str__()
    │
    👥 Reader
    ├── Атрибуты:
    │   ├── name: str
    │   ├── reader_id: str
    │   ├── phone: str
    │   ├── email: str
    │   └── borrowed_books: list
    ├── Методы:
    │   ├── __init__(name, reader_id, phone, email)
    │   ├── borrow_book(book)
    │   ├── return_book(book)
    │   ├── to_dict()
    │   ├── from_dict(data, library)
    │   └── __str__()
    │
    🏛️ Library
    ├── Атрибуты:
    │   ├── books: list
    │   └── readers: list
    ├── Методы:
    │   ├── add_book(book)
    │   ├── register_reader(reader)
    │   ├── find_book_by_isbn(isbn)
    │   ├── find_reader_by_id(reader_id)
    │   ├── lend_book(isbn, reader_id)
    │   ├── return_book(isbn, reader_id)
    │   ├── save_to_file()
    │   └── load_from_file()
    │
    🖥️ LibraryApp (QMainWindow)
    ├── Атрибуты:
    │   ├── library: Library
    │   └── UI элементы
    ├── Методы:
    │   ├── __init__()
    │   ├── setup_styles()
    │   ├── init_ui()
    │   ├── create_books_tab()
    │   ├── create_readers_tab()
    │   ├── create_operations_tab()
    │   ├── create_stats_tab()
    │   └── обработчики событий

    ╔══════════════════════════════════════════╗
    ║              Relationships               ║
    ╚══════════════════════════════════════════╝

    LibraryApp ──contains──► Library
    Library ──contains──► Book, Reader
    Reader ──borrows──► Book
    """

    print(uml_text)

    # Сохраняем в файл
    with open('text_uml_diagram.txt', 'w', encoding='utf-8') as f:
        f.write(uml_text)
    print("✅ Текстовая UML диаграмма сохранена в 'text_uml_diagram.txt'")


def generate_pylint_report():
    """Генерирует отчет pylint"""
    print("\n🔍 Анализ кода с помощью pylint...")
    print("=" * 50)

    files = ['book.py', 'reader.py', 'library.py', 'main_window.py']

    for file in files:
        if os.path.exists(file):
            print(f"\n📊 Анализ {file}:")
            print("-" * 30)

            try:
                result = subprocess.run(
                    ['pylint', '--output-format=text', file],
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                # Выводим только важную информацию
                lines = result.stdout.split('\n')
                for line in lines:
                    if any(keyword in line for keyword in ['rated', 'error', 'warning', 'convention']):
                        print(line)

            except subprocess.TimeoutExpired:
                print("⏰ Таймаут анализа")
            except Exception as e:
                print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    print("🚀 Генерация UML и анализ кода")
    print("=" * 50)

    # 1. Пытаемся сгенерировать графическую UML
    generate_uml_with_pyreverse()

    # 2. Создаем текстовую UML
    create_text_uml()

    # 3. Генерируем отчет pylint
    generate_pylint_report()

    print("\n✅ Все отчеты сгенерированы!")