import json
import os

# ANSI escape codes for styling
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"

class Book:
    def __init__(self, book_id, title, author, year, status="в наличии"):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def __str__(self):
        return f"ID: {self.book_id}, Название: {self.title}, Автор: {self.author}, Год: {self.year}, Статус: {self.status}"

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }

class Library:
    def __init__(self):
        self.books = {}
        self.next_id = 1
        self.load_books()

    def load_books(self):
        if os.path.exists('books.json'):
            try:
                with open('books.json', 'r', encoding='utf-8') as file:
                    books_data = json.load(file)
                    for book_data in books_data:
                        book = Book(**book_data)
                        self.books[book.book_id] = book
                        self.next_id = max(self.next_id, book.book_id + 1)
                print(f"{CYAN}Загружено книг: {len(self.books)}{RESET}")  # Отладочное сообщение
            except json.JSONDecodeError:
                print(f"{RED}Ошибка: файл книг поврежден или имеет неправильный формат.{RESET}")
            except Exception as e:
                print(f"{RED}Ошибка при загрузке книг: {e}{RESET}")

    def save_books(self):
        try:
            with open('books.json', 'w', encoding='utf-8') as file:
                json.dump([book.to_dict() for book in self.books.values()], file, ensure_ascii=False, indent=4)
            print(f"{GREEN}Книги успешно сохранены.{RESET}")  # Отладочное сообщение
        except Exception as e:
            print(f"{RED}Ошибка при сохранении книг: {e}{RESET}")

    def add_book(self, title, author, year):
        try:
            year = int(year)
        except ValueError:
            print(f"{RED}Ошибка: год издания должен быть целым числом.{RESET}")
            return

        book = Book(self.next_id, title, author, year)
        self.books[self.next_id] = book
        print(f"{GREEN}Книга добавлена:{RESET} {book}")
        self.save_books()
        self.next_id += 1

    def remove_book(self, book_id):
        if book_id in self.books:
            removed_book = self.books.pop(book_id)
            print(f"{GREEN}Книга удалена:{RESET} {removed_book}")
            self.save_books()
        else:
            print(f"{RED}Ошибка: Книга с таким ID не найдена.{RESET}")
    
    def update_book_status(self, book_id, new_status):
        if book_id in self.books:
            self.books[book_id].status = new_status
            print(f"{GREEN}Статус книги ID {book_id} изменен на {new_status}.{RESET}")
            self.save_books()
        else:
            print(f"{RED}Ошибка: Книга с таким ID не найдена.{RESET}")
    
    def search_books(self, title=None, author=None, year=None, status=None):
        results = []
        for book in self.books.values():
            if (title is None or title.lower() in book.title.lower()) and \
               (author is None or author.lower() in book.author.lower()) and \
               (year is None or year == book.year) and \
               (status is None or status.lower() == book.status.lower()):
                results.append(book)
        return results

    def display_books(self):
        if not self.books:
            print(f"{YELLOW}Нет доступных книг.{RESET}")
        else:
            print(f"{CYAN}Список доступных книг:{RESET}")
            for book in self.books.values():
                print(book)

def main():
    library = Library()

    while True:
        print("\n" + "=" * 30)
        print(f"{BOLD}МЕНЮ:{RESET}")
        print(f"1. {CYAN}Добавить книгу{RESET}")
        print(f"2. {CYAN}Удалить книгу{RESET}")
        print(f"3. {CYAN}Показать все книги{RESET}")
        print(f"4. {CYAN}Искать книги{RESET}")
        print(f"5. {CYAN}Изменить статус книги{RESET}")
        print(f"6. {CYAN}Выход{RESET}")

        choice = input("ВЫБЕРИТЕ действие (1-6): ")

        if choice == '1':
            title = input("ВВЕДИТЕ название книги: ")
            author = input("ВВЕДИТЕ автора книги: ")
            year = input("ВВЕДИТЕ год издания: ")
            library.add_book(title, author, year)

        elif choice == '2':
            book_id = input("ВВЕДИТЕ ID книги для УДАЛЕНИЯ: ")
            try:
                library.remove_book(int(book_id))
            except ValueError:
                print(f"{RED}Ошибка: Введите корректный ID (целое число).{RESET}")

        elif choice == '3':
            library.display_books()

        elif choice == '4':
            title = input("ВВЕДИТЕ название книги для поиска (оставьте пустым, если не хотите фильтровать): ")
            author = input("ВВЕДИТЕ автора книги для поиска (оставьте пустым, если не хотите фильтровать): ")
            year_input = input("ВВЕДИТЕ год издания для поиска (оставьте пустым, если не хотите фильтровать): ")
            status = input("ВВЕДИТЕ статус книги для поиска (оставьте пустым, если не хотите фильтровать): ")

            year = int(year_input) if year_input else None
            status = status if status else None

            results = library.search_books(
                title=title if title else None,
                author=author if author else None,
                year=year,
                status=status
            )

            if results:
                print(f"{CYAN}НАЙДЕННЫЕ КНИГИ:{RESET}")
                for book in results:
                    print(book)
            else:
                print(f"{YELLOW}Книги не найдены по заданным критериям.{RESET}")

        elif choice == '5':
            book_id = input("ВВЕДИТЕ ID книги для изменения статуса: ")
            new_status = input("ВВЕДИТЕ новый статус книги: ")
            try:
                library.update_book_status(int(book_id), new_status)
            except ValueError:
                print(f"{RED}Ошибка: Введите корректный ID (целое число).{RESET}")

        elif choice == '6':
            print(f"{GREEN}ВЫХОД ИЗ ПРОГРАММЫ.{RESET}")
            break

        else:
            print(f"{RED}НЕВЕРНЫЙ ВЫБОР. ПОЖАЛУЙСТА, ВЫБЕРИТЕ от 1 до 6.{RESET}")

if __name__ == "__main__":
    main()
