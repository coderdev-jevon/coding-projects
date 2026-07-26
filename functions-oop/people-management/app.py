# Plain English Steps
# 1. Make a class called person with attributes name, age, nationality, gender
# 2. Inherit the person class to create student, library and bank system
# 3. Add methods to each to display detailed info about them

class Person:
    def __init__(self, name, age, nationality, gender):
        self.name = name
        self.age = age
        self.nationality = nationality
        self.gender = gender

class Student(Person):
    def __init__(self, name="Jevon", age=18, nationality="Indonesia", gender="Male", grade=13):
        super().__init__(name, age, nationality, gender)
        self.grade = grade
    def student_info(self):
        return f"{self.name} is currently on {self.grade}th grade."

class Patron(Person):
    def __init__(self, name="Jevon", age=18, nationality="Indonesia", gender="Male"):
        super().__init__(name, age, nationality, gender)
        self.total_books = 0
        self.borrowed_books = []
    def add_books(self, books):
        self.borrowed_books.extend(books)
        self.total_books = len(self.borrowed_books)

    def patron_info(self):
        if self.borrowed_books != []:
            return f"The books {self.name} borrowed include {self.borrowed_books}."
        else:
            return f"{self.name} hasn't borrowed any books."

class BankCustomer(Person):
    def __init__(self, name="Jevon", age=18, nationality="Indonesia", gender="Male"):
        super().__init__(name, age, nationality, gender)
        self._income = 0
        self._expense = 0
    def add_income(self, income):
        self._income += income
    def add_expense(self, expense):
        self._expense += expense
    def income(self):
        return self._income
    def expense(self):
        return self._expense
    def bank_info(self):
        return (
            f"{self.name}'s total income is ${self._income}. "
            f"{self.name}'s total expense is ${self._expense}. "
            f"{self.name}'s total bank capital is ${self._income - self._expense}."
        )
jevon = BankCustomer()

print(jevon.bank_info())
