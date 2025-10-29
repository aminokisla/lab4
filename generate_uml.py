import os
import subprocess
import ast
import graphviz
from pathlib import Path


class UMLGenerator:
    def __init__(self, project_path):
        self.project_path = project_path
        self.classes = {}
        self.relationships = []

    def parse_python_files(self):
        """Парсит все Python файлы в проекте и извлекает информацию о классах"""
        python_files = list(Path(self.project_path).glob("**/*.py"))

        for file_path in python_files:
            if file_path.name.startswith('__') or 'test' in file_path.name.lower():
                continue

            with open(file_path, 'r', encoding='utf-8') as file:
                try:
                    tree = ast.parse(file.read(), filename=str(file_path))
                    self._extract_classes_from_ast(tree, file_path)
                except SyntaxError as e:
                    print(f"Ошибка синтаксиса в {file_path}: {e}")

    def _extract_classes_from_ast(self, tree, file_path):
        """Извлекает информацию о классах из AST"""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_info = {
                    'name': node.name,
                    'file': file_path.name,
                    'methods': [],
                    'attributes': [],
                    'bases': []
                }

                # Получаем родительские классы
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        class_info['bases'].append(base.id)

                # Получаем методы и атрибуты
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        class_info['methods'].append(item.name)
                    elif isinstance(item, ast.Assign):
                        for target in item.targets:
                            if isinstance(target, ast.Name):
                                class_info['attributes'].append(target.id)

                self.classes[node.name] = class_info

    def analyze_relationships(self):
        """Анализирует отношения между классами"""
        for class_name, class_info in self.classes.items():
            # Наследование
            for base_class in class_info['bases']:
                if base_class in self.classes:
                    self.relationships.append({
                        'from': class_name,
                        'to': base_class,
                        'type': 'inheritance'
                    })

            # Ассоциации (по использованию в методах)
            for method in class_info['methods']:
                # Упрощенный анализ - ищем упоминания других классов
                pass

    def generate_dot_file(self, output_file='classes.dot'):
        """Генерирует DOT файл для Graphviz"""
        dot = graphviz.Digraph(comment='UML Class Diagram', format='png')
        dot.attr(rankdir='TB', splines='ortho')

        # Создаем узлы для классов
        for class_name, class_info in self.classes.items():
            label = f'{{{class_name}'

            # Добавляем атрибуты
            if class_info['attributes']:
                label += '|' + '\\n'.join([f'+ {attr}' for attr in class_info['attributes']])

            # Добавляем методы
            if class_info['methods']:
                label += '|' + '\\n'.join([f'+ {method}()' for method in class_info['methods']])

            label += '}'

            dot.node(class_name, label, shape='record', style='filled',
                     fillcolor='lightblue', fontname='Arial')

        # Добавляем отношения
        for rel in self.relationships:
            if rel['type'] == 'inheritance':
                dot.edge(rel['from'], rel['to'], arrowhead='onormal',
                         style='dashed', color='darkgreen')

        # Сохраняем DOT файл
        dot.save(output_file)
        return output_file

    def generate_diagram(self, output_file='class_diagram'):
        """Генерирует финальную диаграмму"""
        dot_file = self.generate_dot_file()

        # Конвертируем DOT в PNG
        try:
            graphviz.render('dot', 'png', dot_file)
            print(f"✅ Диаграмма сохранена как {output_file}.png")
        except Exception as e:
            print(f"❌ Ошибка при генерации диаграммы: {e}")
            print("Убедитесь, что Graphviz установлен и добавлен в PATH")


def run_pylint_analysis():
    """Запускает анализ кода с помощью pylint"""
    print("🔍 Запуск анализа кода с помощью pylint...")

    commands = [
        ['pylint', '--reports=y', '--output-format=text', 'book.py'],
        ['pylint', '--reports=y', '--output-format=text', 'reader.py'],
        ['pylint', '--reports=y', '--output-format=text', 'library.py'],
        ['pylint', '--reports=y', '--output-format=text', 'main_window.py']
    ]

    for cmd in commands:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            print(f"\n{'=' * 50}")
            print(f"Анализ {cmd[-1]}:")
            print(result.stdout)
            if result.stderr:
                print("Ошибки:", result.stderr)
        except Exception as e:
            print(f"Ошибка при анализе {cmd[-1]}: {e}")


def main():
    """Основная функция"""
    print("🚀 Генерация UML диаграммы классов и анализ кода")
    print("=" * 50)

    # 1. Анализ кода с pylint
    run_pylint_analysis()

    # 2. Генерация UML диаграммы
    print("\n📊 Генерация UML диаграммы классов...")

    generator = UMLGenerator('.')
    generator.parse_python_files()
    generator.analyze_relationships()
    generator.generate_diagram()

    print("\n✅ Все задачи выполнены!")
    print("📁 Результаты:")
    print("   - Анализ кода: вывод в консоли")
    print("   - UML диаграмма: class_diagram.png")


if __name__ == "__main__":
    main()