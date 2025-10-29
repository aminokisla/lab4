"""
Модуль для работы с книгами в библиотечной системе.

Содержит класс Book, представляющий книгу с основными атрибутами
и методами для сериализации/десериализации.
"""


class Book:
    """
    Класс, представляющий книгу в библиотечной системе.

    Attributes:
        title (str): Название книги
        author (str): Автор книги
        isbn (str): Уникальный идентификатор книги (ISBN)
        year (int): Год издания книги
        is_available (bool): Флаг доступности книги для выдачи

    Examples:
        >>> book = Book("Преступление и наказание", "Ф.М. Достоевский", "123-456", 1866)
        >>> print(book)
        'Преступление и наказание' - Ф.М. Достоевский (1866) [ISBN: 123-456] - Доступна
    """

    task_id_counter = 1

    def __init__(self, title, author, isbn, year=None):
        """
        Инициализирует объект книги.

        Args:
            title (str): Название книги
            author (str): Автор книги
            isbn (str): ISBN книги
            year (int, optional): Год издания. Defaults to None.

        Raises:
            ValueError: Если title, author или isbn пустые
        """
        if not title or not author or not isbn:
            raise ValueError("Название, автор и ISBN не могут быть пустыми")

        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year
        self.is_available = True

    def to_dict(self):
        """
        Преобразует объект книги в словарь для сериализации.

        Returns:
            dict: Словарь с данными книги, включая:
                - title (str): Название
                - author (str): Автор
                - isbn (str): ISBN
                - year (int): Год издания
                - is_available (bool): Доступность

        Example:
            >>> book = Book("Мастер и Маргарита", "М.А. Булгаков", "789-012")
            >>> book_dict = book.to_dict()
            >>> print(book_dict['title'])
            Мастер и Маргарита
        """
        return {
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'year': self.year,
            'is_available': self.is_available
        }

    @classmethod
    def from_dict(cls, data):
        """
        Создает объект книги из словаря.

        Args:
            data (dict): Словарь с данными книги

        Returns:
            Book: Новый объект книги

        Raises:
            KeyError: Если в словаре отсутствуют обязательные поля
        """
        return cls(data['title'], data['author'], data['isbn'], data.get('year'))

    def mark_as_borrowed(self):
        """Помечает книгу как выданную."""
        self.is_available = False

    def mark_as_available(self):
        """Помечает книгу как доступную."""
        self.is_available = True

    def __str__(self):
        """
        Возвращает строковое представление книги.

        Returns:
            str: Строка в формате: 'Название' - Автор (Год) [ISBN: XXX] - Статус
        """
        status = "Доступна" if self.is_available else "Выдана"
        year_info = f" ({self.year})" if self.year else ""
        return f"'{self.title}' - {self.author}{year_info} [ISBN: {self.isbn}] - {status}"

    def __repr__(self):
        """Возвращает представление книги для отладки."""
        return f"Book(title='{self.title}', author='{self.author}', isbn='{self.isbn}')"