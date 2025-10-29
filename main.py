import sys
from PyQt6.QtWidgets import QApplication
from main_window import LibraryApp

def main():
    app = QApplication(sys.argv)
    window = LibraryApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()