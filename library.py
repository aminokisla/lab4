import json
from book import Book
from reader import Reader


class Library:
    def __init__(self):
        self.books = []
        self.readers = []

    def add_book(self, book):
        self.books.append(book)
        return f"Книга '{book.title}' добавлена в библиотеку"

    def register_reader(self, reader):
        self.readers.append(reader)
        return f"Читатель {reader.name} зарегистрирован"

    def find_book_by_isbn(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def find_reader_by_id(self, reader_id):
        for reader in self.readers:
            if reader.reader_id == reader_id:
                return reader
        return None

    def get_all_books(self):
        return self.books

    def get_available_books(self):
        return [book for book in self.books if book.is_available]

    def get_all_readers(self):
        return self.readers

    def find_books_by_author(self, author):
        return [book for book in self.books if author.lower() in book.author.lower()]

    def find_books_by_title(self, title):
        return [book for book in self.books if title.lower() in book.title.lower()]

    def lend_book(self, isbn, reader_id):
        book = self.find_book_by_isbn(isbn)
        reader = self.find_reader_by_id(reader_id)

        if not book:
            return "Книга не найдена"
        if not reader:
            return "Читатель не найден"
        if not book.is_available:
            return "Книга уже выдана"

        if reader.borrow_book(book):
            return f"Книга '{book.title}' выдана читателю {reader.name}"
        return "Ошибка при выдаче книги"

    def return_book(self, isbn, reader_id):
        book = self.find_book_by_isbn(isbn)
        reader = self.find_reader_by_id(reader_id)

        if not book:
            return "Книга не найдена"
        if not reader:
            return "Читатель не найден"

        if reader.return_book(book):
            return f"Книга '{book.title}' возвращена в библиотеку"
        return "Эта книга не была выдана данному читателю"

    def save_to_file(self, filename="library_data.json"):
        data = {
            'books': [book.to_dict() for book in self.books],
            'readers': [reader.to_dict() for reader in self.readers]
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_from_file(self, filename="library_data.json"):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.books = [Book.from_dict(book_data) for book_data in data.get('books', [])]
            self.readers = [Reader.from_dict(reader_data, self) for reader_data in data.get('readers', [])]
            return True
        except FileNotFoundError:
            return False