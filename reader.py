class Reader:
    def __init__(self, name, reader_id, phone=None, email=None):
        self.name = name
        self.reader_id = reader_id
        self.phone = phone
        self.email = email
        self.borrowed_books = []

    def borrow_book(self, book):
        if book.is_available:
            self.borrowed_books.append(book)
            book.is_available = False
            return True
        return False

    def return_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            book.is_available = True
            return True
        return False

    def to_dict(self):
        return {
            'name': self.name,
            'reader_id': self.reader_id,
            'phone': self.phone,
            'email': self.email,
            'borrowed_books_isbns': [book.isbn for book in self.borrowed_books]
        }

    @classmethod
    def from_dict(cls, data, library):
        reader = cls(data['name'], data['reader_id'], data.get('phone'), data.get('email'))
        # Восстанавливаем взятые книги из библиотеки
        for isbn in data.get('borrowed_books_isbns', []):
            book = library.find_book_by_isbn(isbn)
            if book:
                reader.borrowed_books.append(book)
                book.is_available = False
        return reader

    def __str__(self):
        return f"{self.name} (ID: {self.reader_id})"