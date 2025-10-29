from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTabWidget, QTableWidget, QTableWidgetItem,
                             QPushButton, QLineEdit, QTextEdit, QLabel,
                             QMessageBox, QComboBox, QHeaderView, QGroupBox,
                             QFormLayout, QFrame, QSplitter)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor
from library import Library
from book import Book
from reader import Reader


class LibraryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.library = Library()
        self.library.load_from_file()

        self.setup_styles()
        self.init_ui()
        self.load_data_to_tables()

    def setup_styles(self):
        """Настройка цветовой схемы и стилей"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
            }
            QTabWidget::pane {
                border: 1px solid #c4c7c5;
                background-color: white;
                border-radius: 4px;
            }
            QTabBar::tab {
                background-color: #e1e5ea;
                color: #2c3e50;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #3498db;
                color: white;
            }
            QTabBar::tab:hover {
                background-color: #2980b9;
                color: white;
            }
            QGroupBox {
                font-weight: bold;
                font-size: 12px;
                color: #2c3e50;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QPushButton.success {
                background-color: #27ae60;
            }
            QPushButton.success:hover {
                background-color: #219653;
            }
            QPushButton.warning {
                background-color: #e67e22;
            }
            QPushButton.warning:hover {
                background-color: #d35400;
            }
            QLineEdit, QComboBox {
                padding: 6px;
                border: 2px solid #bdc3c7;
                border-radius: 4px;
                background-color: white;
                font-size: 12px;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #3498db;
            }
            QTableWidget {
                gridline-color: #bdc3c7;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: white;
                alternate-background-color: #f8f9fa;
            }
            QTableWidget::item {
                padding: 6px;
                border-bottom: 1px solid #ecf0f1;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QTextEdit {
                border: 2px solid #bdc3c7;
                border-radius: 4px;
                background-color: white;
                font-family: 'Courier New';
                font-size: 11px;
            }
            QLabel {
                color: #2c3e50;
                font-weight: bold;
            }
            QLabel.title {
                font-size: 14px;
                color: #3498db;
                padding: 5px;
            }
        """)

    def init_ui(self):
        self.setWindowTitle("📚 Система управления библиотекой")
        self.setGeometry(100, 100, 1200, 800)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Заголовок
        title_label = QLabel("📖 Библиотечная система управления")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
                background-color: #3498db;
                color: white;
                border-radius: 8px;
            }
        """)
        layout.addWidget(title_label)

        # Создаем вкладки
        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        layout.addWidget(tabs)

        # Вкладки
        books_tab = self.create_books_tab()
        readers_tab = self.create_readers_tab()
        operations_tab = self.create_operations_tab()
        stats_tab = self.create_stats_tab()

        tabs.addTab(books_tab, "📕 Книги")
        tabs.addTab(readers_tab, "👥 Читатели")
        tabs.addTab(operations_tab, "🔄 Операции")
        tabs.addTab(stats_tab, "📊 Статистика")

        # Панель управления внизу
        control_layout = QHBoxLayout()

        save_btn = QPushButton("💾 Сохранить данные")
        save_btn.setProperty("class", "success")
        save_btn.clicked.connect(self.save_data)

        refresh_btn = QPushButton("🔄 Обновить")
        refresh_btn.clicked.connect(self.load_data_to_tables)

        control_layout.addWidget(save_btn)
        control_layout.addWidget(refresh_btn)
        control_layout.addStretch()

        layout.addLayout(control_layout)

    def create_books_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)

        # Группа добавления книги
        add_group = QGroupBox("Добавить новую книгу")
        add_layout = QFormLayout(add_group)
        add_layout.setVerticalSpacing(10)
        add_layout.setHorizontalSpacing(15)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Введите название книги...")

        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Введите автора...")

        self.isbn_input = QLineEdit()
        self.isbn_input.setPlaceholderText("Введите ISBN...")

        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("Год издания (необязательно)")

        add_layout.addRow("📖 Название:", self.title_input)
        add_layout.addRow("✍️ Автор:", self.author_input)
        add_layout.addRow("🏷️ ISBN:", self.isbn_input)
        add_layout.addRow("📅 Год:", self.year_input)

        add_book_btn = QPushButton("➕ Добавить книгу")
        add_book_btn.setProperty("class", "success")
        add_book_btn.clicked.connect(self.add_book)
        add_layout.addRow(add_book_btn)

        # Таблица книг
        table_group = QGroupBox("Список книг в библиотеке")
        table_layout = QVBoxLayout(table_group)

        self.books_table = QTableWidget()
        self.books_table.setColumnCount(5)
        self.books_table.setHorizontalHeaderLabels(["Название", "Автор", "ISBN", "Год", "Статус"])
        self.books_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.books_table.setAlternatingRowColors(True)

        table_layout.addWidget(self.books_table)

        layout.addWidget(add_group)
        layout.addWidget(table_group)

        return widget

    def create_readers_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)

        # Группа добавления читателя
        add_group = QGroupBox("Добавить нового читателя")
        add_layout = QFormLayout(add_group)
        add_layout.setVerticalSpacing(10)
        add_layout.setHorizontalSpacing(15)

        self.reader_name_input = QLineEdit()
        self.reader_name_input.setPlaceholderText("Введите ФИО читателя...")

        self.reader_id_input = QLineEdit()
        self.reader_id_input.setPlaceholderText("Уникальный идентификатор...")

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Номер телефона...")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email адрес...")

        add_layout.addRow("👤 ФИО:", self.reader_name_input)
        add_layout.addRow("🆔 ID читателя:", self.reader_id_input)
        add_layout.addRow("📞 Телефон:", self.phone_input)
        add_layout.addRow("📧 Email:", self.email_input)

        add_reader_btn = QPushButton("➕ Добавить читателя")
        add_reader_btn.setProperty("class", "success")
        add_reader_btn.clicked.connect(self.add_reader)
        add_layout.addRow(add_reader_btn)

        # Таблица читателей
        table_group = QGroupBox("Зарегистрированные читатели")
        table_layout = QVBoxLayout(table_group)

        self.readers_table = QTableWidget()
        self.readers_table.setColumnCount(4)
        self.readers_table.setHorizontalHeaderLabels(["ФИО", "ID", "Телефон", "Email"])
        self.readers_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.readers_table.setAlternatingRowColors(True)

        table_layout.addWidget(self.readers_table)

        layout.addWidget(add_group)
        layout.addWidget(table_group)

        return widget

    def create_operations_tab(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setSpacing(20)

        # Левая панель - операции
        left_panel = QFrame()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(15)

        # Выдача книги
        lend_group = QGroupBox("📤 Выдача книги")
        lend_layout = QFormLayout(lend_group)
        lend_layout.setVerticalSpacing(10)

        self.lend_isbn_input = QLineEdit()
        self.lend_isbn_input.setPlaceholderText("ISBN книги...")

        self.lend_reader_id_input = QLineEdit()
        self.lend_reader_id_input.setPlaceholderText("ID читателя...")

        lend_layout.addRow("🏷️ ISBN книги:", self.lend_isbn_input)
        lend_layout.addRow("🆔 ID читателя:", self.lend_reader_id_input)

        lend_btn = QPushButton("📤 Выдать книгу")
        lend_btn.clicked.connect(self.lend_book)
        lend_layout.addRow(lend_btn)

        # Возврат книги
        return_group = QGroupBox("📥 Возврат книги")
        return_layout = QFormLayout(return_group)
        return_layout.setVerticalSpacing(10)

        self.return_isbn_input = QLineEdit()
        self.return_isbn_input.setPlaceholderText("ISBN книги...")

        self.return_reader_id_input = QLineEdit()
        self.return_reader_id_input.setPlaceholderText("ID читателя...")

        return_layout.addRow("🏷️ ISBN книги:", self.return_isbn_input)
        return_layout.addRow("🆔 ID читателя:", self.return_reader_id_input)

        return_btn = QPushButton("📥 Вернуть книгу")
        return_btn.clicked.connect(self.return_book)
        return_layout.addRow(return_btn)

        # Поиск книг
        search_group = QGroupBox("🔍 Поиск книг")
        search_layout = QVBoxLayout(search_group)

        search_type_layout = QHBoxLayout()
        search_type_layout.addWidget(QLabel("Поиск по:"))
        self.search_type = QComboBox()
        self.search_type.addItems(["Автору", "Названию"])
        search_type_layout.addWidget(self.search_type)
        search_type_layout.addStretch()

        search_term_layout = QHBoxLayout()
        search_term_layout.addWidget(QLabel("Запрос:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите текст для поиска...")
        search_term_layout.addWidget(self.search_input)

        search_btn = QPushButton("🔍 Найти книги")
        search_btn.clicked.connect(self.search_books)

        search_layout.addLayout(search_type_layout)
        search_layout.addLayout(search_term_layout)
        search_layout.addWidget(search_btn)

        left_layout.addWidget(lend_group)
        left_layout.addWidget(return_group)
        left_layout.addWidget(search_group)
        left_layout.addStretch()

        # Правая панель - результаты
        right_panel = QFrame()
        right_layout = QVBoxLayout(right_panel)

        results_group = QGroupBox("📋 Результаты поиска")
        results_layout = QVBoxLayout(results_group)

        self.search_results = QTextEdit()
        self.search_results.setMinimumHeight(400)
        self.search_results.setPlaceholderText("Здесь будут отображаться результаты поиска...")

        results_layout.addWidget(self.search_results)

        right_layout.addWidget(results_group)

        layout.addWidget(left_panel)
        layout.addWidget(right_panel)
        layout.setStretchFactor(left_panel, 1)
        layout.setStretchFactor(right_panel, 2)

        return widget

    def create_stats_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)

        # Статистика в виде карточек
        stats_group = QGroupBox("📊 Статистика библиотеки")
        stats_layout = QHBoxLayout(stats_group)

        # Карточка книг
        books_card = QFrame()
        books_card.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                border-radius: 8px;
                padding: 15px;
            }
            QLabel {
                color: white;
                font-weight: bold;
            }
        """)
        books_layout = QVBoxLayout(books_card)
        books_title = QLabel("📚 Всего книг")
        books_title.setStyleSheet("font-size: 14px;")
        books_count = QLabel("0")
        books_count.setStyleSheet("font-size: 24px; font-weight: bold;")
        books_layout.addWidget(books_title)
        books_layout.addWidget(books_count)
        books_layout.addStretch()

        # Карточка читателей
        readers_card = QFrame()
        readers_card.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #27ae60, stop:1 #219653);
                border-radius: 8px;
                padding: 15px;
            }
            QLabel {
                color: white;
                font-weight: bold;
            }
        """)
        readers_layout = QVBoxLayout(readers_card)
        readers_title = QLabel("👥 Зарегистрировано читателей")
        readers_title.setStyleSheet("font-size: 14px;")
        readers_count = QLabel("0")
        readers_count.setStyleSheet("font-size: 24px; font-weight: bold;")
        readers_layout.addWidget(readers_title)
        readers_layout.addWidget(readers_count)
        readers_layout.addStretch()

        # Карточка доступных книг
        available_card = QFrame()
        available_card.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e67e22, stop:1 #d35400);
                border-radius: 8px;
                padding: 15px;
            }
            QLabel {
                color: white;
                font-weight: bold;
            }
        """)
        available_layout = QVBoxLayout(available_card)
        available_title = QLabel("✅ Доступно книг")
        available_title.setStyleSheet("font-size: 14px;")
        available_count = QLabel("0")
        available_count.setStyleSheet("font-size: 24px; font-weight: bold;")
        available_layout.addWidget(available_title)
        available_layout.addWidget(available_count)
        available_layout.addStretch()

        stats_layout.addWidget(books_card)
        stats_layout.addWidget(readers_card)
        stats_layout.addWidget(available_card)

        # Таблица последних операций
        recent_group = QGroupBox("📝 Последние книги")
        recent_layout = QVBoxLayout(recent_group)

        self.recent_books_table = QTableWidget()
        self.recent_books_table.setColumnCount(4)
        self.recent_books_table.setHorizontalHeaderLabels(["Название", "Автор", "ISBN", "Статус"])
        self.recent_books_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.recent_books_table.setAlternatingRowColors(True)

        recent_layout.addWidget(self.recent_books_table)

        layout.addWidget(stats_group)
        layout.addWidget(recent_group)

        # Сохраняем ссылки для обновления
        self.books_count_label = books_count
        self.readers_count_label = readers_count
        self.available_count_label = available_count

        return widget

    # Далее идут все методы из предыдущей версии (add_book, add_reader, lend_book, return_book, search_books, load_data_to_tables и т.д.)
    # Я их не менял, поэтому просто вставлю их обратно:

    def add_book(self):
        title = self.title_input.text().strip()
        author = self.author_input.text().strip()
        isbn = self.isbn_input.text().strip()
        year = self.year_input.text().strip()

        if not title or not author or not isbn:
            QMessageBox.warning(self, "Ошибка", "Заполните обязательные поля: название, автор, ISBN")
            return

        if self.library.find_book_by_isbn(isbn):
            QMessageBox.warning(self, "Ошибка", "Книга с таким ISBN уже существует")
            return

        year_int = int(year) if year.isdigit() else None
        book = Book(title, author, isbn, year_int)
        result = self.library.add_book(book)

        QMessageBox.information(self, "Успех", result)
        self.clear_book_form()
        self.load_data_to_tables()

    def add_reader(self):
        name = self.reader_name_input.text().strip()
        reader_id = self.reader_id_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()

        if not name or not reader_id:
            QMessageBox.warning(self, "Ошибка", "Заполните обязательные поля: имя, ID читателя")
            return

        if self.library.find_reader_by_id(reader_id):
            QMessageBox.warning(self, "Ошибка", "Читатель с таким ID уже существует")
            return

        reader = Reader(name, reader_id, phone, email)
        result = self.library.register_reader(reader)

        QMessageBox.information(self, "Успех", result)
        self.clear_reader_form()
        self.load_data_to_tables()

    def lend_book(self):
        isbn = self.lend_isbn_input.text().strip()
        reader_id = self.lend_reader_id_input.text().strip()

        if not isbn or not reader_id:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return

        result = self.library.lend_book(isbn, reader_id)
        QMessageBox.information(self, "Результат", result)
        self.lend_isbn_input.clear()
        self.lend_reader_id_input.clear()
        self.load_data_to_tables()

    def return_book(self):
        isbn = self.return_isbn_input.text().strip()
        reader_id = self.return_reader_id_input.text().strip()

        if not isbn or not reader_id:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return

        result = self.library.return_book(isbn, reader_id)
        QMessageBox.information(self, "Результат", result)
        self.return_isbn_input.clear()
        self.return_reader_id_input.clear()
        self.load_data_to_tables()

    def search_books(self):
        search_term = self.search_input.text().strip()
        if not search_term:
            QMessageBox.warning(self, "Ошибка", "Введите поисковый запрос")
            return

        search_type = self.search_type.currentText()
        if search_type == "Автору":
            results = self.library.find_books_by_author(search_term)
        else:
            results = self.library.find_books_by_title(search_term)

        if results:
            result_text = f"🔍 Найдено {len(results)} книг:\n\n"
            for book in results:
                status = "✅ Доступна" if book.is_available else "❌ Выдана"
                result_text += f"• {book.title} - {book.author} [{status}]\n"
            self.search_results.setText(result_text)
        else:
            self.search_results.setText("❌ Книги не найдены")

    def load_data_to_tables(self):
        self.load_books_table()
        self.load_readers_table()
        self.load_stats()
        self.load_recent_books()

    def load_books_table(self):
        books = self.library.get_all_books()
        self.books_table.setRowCount(len(books))

        for row, book in enumerate(books):
            self.books_table.setItem(row, 0, QTableWidgetItem(book.title))
            self.books_table.setItem(row, 1, QTableWidgetItem(book.author))
            self.books_table.setItem(row, 2, QTableWidgetItem(book.isbn))
            self.books_table.setItem(row, 3, QTableWidgetItem(str(book.year) if book.year else ""))
            status = "✅ Доступна" if book.is_available else "❌ Выдана"
            status_item = QTableWidgetItem(status)
            if book.is_available:
                status_item.setBackground(QColor(39, 174, 96, 50))
            else:
                status_item.setBackground(QColor(231, 76, 60, 50))
            self.books_table.setItem(row, 4, status_item)

    def load_readers_table(self):
        readers = self.library.get_all_readers()
        self.readers_table.setRowCount(len(readers))

        for row, reader in enumerate(readers):
            self.readers_table.setItem(row, 0, QTableWidgetItem(reader.name))
            self.readers_table.setItem(row, 1, QTableWidgetItem(reader.reader_id))
            self.readers_table.setItem(row, 2, QTableWidgetItem(reader.phone if reader.phone else ""))
            self.readers_table.setItem(row, 3, QTableWidgetItem(reader.email if reader.email else ""))

    def load_stats(self):
        """Загрузка статистики"""
        total_books = len(self.library.get_all_books())
        total_readers = len(self.library.get_all_readers())
        available_books = len(self.library.get_available_books())

        self.books_count_label.setText(str(total_books))
        self.readers_count_label.setText(str(total_readers))
        self.available_count_label.setText(str(available_books))

    def load_recent_books(self):
        """Загрузка последних книг"""
        books = self.library.get_all_books()[:10]  # Последние 10 книг
        self.recent_books_table.setRowCount(len(books))

        for row, book in enumerate(books):
            self.recent_books_table.setItem(row, 0, QTableWidgetItem(book.title))
            self.recent_books_table.setItem(row, 1, QTableWidgetItem(book.author))
            self.recent_books_table.setItem(row, 2, QTableWidgetItem(book.isbn))
            status = "✅ Доступна" if book.is_available else "❌ Выдана"
            status_item = QTableWidgetItem(status)
            if book.is_available:
                status_item.setBackground(QColor(39, 174, 96, 50))
            else:
                status_item.setBackground(QColor(231, 76, 60, 50))
            self.recent_books_table.setItem(row, 3, status_item)

    def clear_book_form(self):
        self.title_input.clear()
        self.author_input.clear()
        self.isbn_input.clear()
        self.year_input.clear()

    def clear_reader_form(self):
        self.reader_name_input.clear()
        self.reader_id_input.clear()
        self.phone_input.clear()
        self.email_input.clear()

    def save_data(self):
        self.library.save_to_file()
        QMessageBox.information(self, "Успех", "✅ Данные успешно сохранены!")

    def closeEvent(self, event):
        self.save_data()
        event.accept()