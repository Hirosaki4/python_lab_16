# ========== ІМПОРТИ ==========
import datetime                   # Модуль для роботи з датами
import json                       # Модуль для експорту JSON
from collections import Counter   # Для підрахунку популярності книг

# ========== ЗАВДАННЯ 1: Основні компоненти бібліотеки ==========

# Клас автора
class Author:
    def __init__(self, name):
        self.name = name  # Ініціалізуємо ім’я автора

# Клас книги
class Book:
    def __init__(self, title, author):
        self.title = title              # Назва книги
        self.author = author            # Автор (об'єкт Author)
        self.is_borrowed = False        # Статус: книга видана чи ні

# Клас бібліотеки
class Library:
    def __init__(self):
        self.books = []                 # Список книг у бібліотеці
        self.borrow_history = []        # Історія видач книг

    def add_book(self, book):
        self.books.append(book)         # Додає книгу до бібліотеки

    def remove_book(self, title):
        self.books = [b for b in self.books if b.title != title]  # Видаляє книгу за назвою

    def find_books(self, query):
        return [b for b in self.books if query.lower() in b.title.lower()]  # Пошук книг за частиною назви

# ========== ЗАВДАННЯ 2: Ведення історії видачі книг ==========

    def borrow_book(self, title, borrower):
        for book in self.books:
            if book.title == title and not book.is_borrowed:
                book.is_borrowed = True                             # Позначаємо книгу як видану
                self.borrow_history.append({
                    'title': title,
                    'borrower': borrower,
                    'borrow_date': datetime.datetime.now(),        # Дата видачі
                    'return_date': None                            # Книга ще не повернута
                })
                return True
        return False                                                # Книгу не знайдено або вже видана

    def return_book(self, title, borrower):
        for record in self.borrow_history:
            if record['title'] == title and record['borrower'] == borrower and record['return_date'] is None:
                record['return_date'] = datetime.datetime.now()     # Фіксуємо дату повернення
                for book in self.books:
                    if book.title == title:
                        book.is_borrowed = False                    # Знімаємо статус "видано"
                return True
        return False                                                # Не знайдено відповідний запис

# ========== ЗАВДАННЯ 3: Статистика бібліотеки ==========

    def get_statistics(self):
        popular = Counter([r['title'] for r in self.borrow_history])        # Підрахунок популярності книг
        total = len(self.borrow_history)                                    # Усього видач
        returned = len([r for r in self.borrow_history if r['return_date']])# Кількість повернень
        return_percentage = (returned / total) * 100 if total > 0 else 0    # Відсоток повернення

        read_times = []
        for r in self.borrow_history:
            if r['return_date']:
                duration = (r['return_date'] - r['borrow_date']).total_seconds() / 3600  # Час читання в годинах
                read_times.append(duration)

        average_time = sum(read_times) / len(read_times) if read_times else 0           # Середній час читання

        return {
            'most_popular': popular.most_common(3),            # Топ-3 книги
            'return_rate': return_percentage,                  # Відсоток повернення книг
            'average_read_time_hours': round(average_time, 2)  # Середній час читання
        }

    def export_statistics_to_json(self, filename='stats.json'):
        stats = self.get_statistics()                          # Отримуємо статистику
        with open(filename, 'w') as f:
            json.dump(stats, f, indent=4)                      # Зберігаємо у JSON-файл

# ========== ДЕМОНСТРАЦІЯ РОБОТИ ==========

if __name__ == "__main__":
    lib = Library()                              # Створюємо бібліотеку

    author1 = Author("Іван Франко")              # Створюємо автора
    author2 = Author("Леся Українка")            # Ще один автор

    book1 = Book("Захар Беркут", author1)        # Створюємо книгу
    book2 = Book("Лісова пісня", author2)        # Друга книга

    lib.add_book(book1)                          # Додаємо першу книгу
    lib.add_book(book2)                          # Додаємо другу книгу

    lib.borrow_book("Захар Беркут", "Оксана")    # Видаємо книгу Оксані
    lib.return_book("Захар Беркут", "Оксана")    # Оксана повертає книгу

    lib.borrow_book("Лісова пісня", "Ігор")      # Ігор бере іншу книгу
    lib.return_book("Лісова пісня", "Ігор")      # Ігор її повертає

    print("Статистика бібліотеки:")
    print(lib.get_statistics())                  # Виводимо статистику в консоль

    lib.export_statistics_to_json()              # Експортуємо статистику у JSON
