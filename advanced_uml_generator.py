import ast
import inspect
import graphviz
from pathlib import Path

from generate_uml import UMLGenerator


class AdvancedUMLGenerator:
    def __init__(self):
        self.classes = {}
        self.relationships = []

    def analyze_class_dependencies(self, class_obj):
        """Анализирует зависимости класса"""
        dependencies = set()

        try:
            source = inspect.getsource(class_obj)
            tree = ast.parse(source)

            for node in ast.walk(tree):
                # Ищем использование других классов в аннотациях типов
                if isinstance(node, ast.AnnAssign):
                    if isinstance(node.annotation, ast.Name):
                        dependencies.add(node.annotation.id)

                # Ищем создание объектов других классов
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        dependencies.add(node.func.id)

                # Ищем атрибуты с типами
                if isinstance(node, ast.Attribute):
                    if isinstance(node.value, ast.Name):
                        dependencies.add(node.value.id)

        except (TypeError, OSError):
            pass

        return dependencies

    def generate_enhanced_diagram(self):
        """Генерирует улучшенную диаграмму"""
        # Динамически импортируем классы
        try:
            from book import Book
            from reader import Reader
            from library import Library
            from main_window import LibraryApp

            classes_to_analyze = [Book, Reader, Library, LibraryApp]

            for cls in classes_to_analyze:
                class_name = cls.__name__
                methods = [method for method in dir(cls)
                           if not method.startswith('_') and callable(getattr(cls, method))]
                attributes = [attr for attr in dir(cls)
                              if not attr.startswith('_') and not callable(getattr(cls, attr))]

                dependencies = self.analyze_class_dependencies(cls)

                self.classes[class_name] = {
                    'methods': methods,
                    'attributes': attributes,
                    'dependencies': dependencies
                }

                # Добавляем отношения наследования
                for base in cls.__bases__:
                    if base.__name__ != 'object':
                        self.relationships.append({
                            'from': class_name,
                            'to': base.__name__,
                            'type': 'inheritance'
                        })

                # Добавляем зависимости
                for dep in dependencies:
                    if dep in [c.__name__ for c in classes_to_analyze]:
                        self.relationships.append({
                            'from': class_name,
                            'to': dep,
                            'type': 'dependency'
                        })

            self._create_enhanced_dot_file()

        except ImportError as e:
            print(f"Ошибка импорта: {e}")

    def _create_enhanced_dot_file(self):
        """Создает улучшенный DOT файл"""
        dot = graphviz.Digraph(comment='Enhanced UML Class Diagram')
        dot.attr(rankdir='TB', splines='ortho')

        # Цвета для разных типов классов
        colors = {
            'Book': 'lightblue',
            'Reader': 'lightgreen',
            'Library': 'lightyellow',
            'LibraryApp': 'lightcoral'
        }

        for class_name, info in self.classes.items():
            # Формируем label для класса
            label = f'{{{class_name}'

            # Атрибуты
            if info['attributes']:
                attrs = '\\n'.join([f'+ {attr}' for attr in info['attributes'][:5]])  # Ограничиваем количество
                label += f'|{attrs}'

            # Методы
            if info['methods']:
                methods = '\\n'.join([f'+ {method}()' for method in info['methods'][:8]])  # Ограничиваем количество
                label += f'|{methods}'

            label += '}'

            # Создаем узел
            color = colors.get(class_name, 'lightgray')
            dot.node(class_name, label, shape='record', style='filled',
                     fillcolor=color, fontname='Arial', fontsize='10')

        # Добавляем отношения
        for rel in self.relationships:
            if rel['type'] == 'inheritance':
                dot.edge(rel['from'], rel['to'], arrowhead='onormal',
                         style='dashed', color='darkgreen')
            elif rel['type'] == 'dependency':
                dot.edge(rel['from'], rel['to'], arrowhead='open',
                         style='dashed', color='blue')

        # Сохраняем
        dot.render('enhanced_class_diagram', format='png', cleanup=True)
        print("✅ Улучшенная диаграмма сохранена как enhanced_class_diagram.png")


def generate_pylint_report():
    """Генерирует подробный отчет pylint"""
    import subprocess

    print("📋 Генерация отчета pylint...")

    # Создаем конфигурационный файл pylint
    pylint_config = """
[MESSAGES CONTROL]
disable=C0103,C0301,R0903,R0913,R0914

[REPORTS]
output-format=text
reports=yes
"""

    with open('.pylintrc', 'w') as f:
        f.write(pylint_config)

    # Запускаем анализ для каждого файла
    files = ['book.py', 'reader.py', 'library.py', 'main_window.py', 'main.py']

    for file in files:
        if Path(file).exists():
            print(f"\n{'=' * 60}")
            print(f"АНАЛИЗ {file}")
            print('=' * 60)

            try:
                result = subprocess.run([
                    'pylint', '--rcfile=.pylintrc', file
                ], capture_output=True, text=True)

                print(result.stdout)

                if result.returncode != 0:
                    print("Предупреждения или ошибки обнаружены")

            except Exception as e:
                print(f"Ошибка при анализе {file}: {e}")


if __name__ == "__main__":
    # Генерация отчетов
    generate_pylint_report()

    # Генерация UML диаграмм
    print("\n🎨 Генерация UML диаграмм...")

    # Простая диаграмма
    simple_gen = UMLGenerator('.')
    simple_gen.parse_python_files()
    simple_gen.analyze_relationships()
    simple_gen.generate_diagram('simple_class_diagram')

    # Улучшенная диаграмма
    advanced_gen = AdvancedUMLGenerator()
    advanced_gen.generate_enhanced_diagram()

    print("\n🎉 Все диаграммы и отчеты сгенерированы!")