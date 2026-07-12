# oop_demo.py – Corey Schafer OOP Parts 1–4
# Classes, instance/class variables, classmethods, staticmethods

print("===== PART 1: CLASSES & INSTANCES =====")


class Employee:
    # Constructor (__init__)
    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = f"{first}.{last}@company.com"

    def fullname(self):
        return f"{self.first} {self.last}"


# Create instances
emp1 = Employee("Ryan", "Kaushal", 50000)
emp2 = Employee("Test", "User", 60000)

print(emp1.email)  # Ryan.Kaushal@company.com
print(emp1.fullname())  # Ryan Kaushal
print(Employee.fullname(emp1))  # Same, but calling via class

print("\n===== PART 2: CLASS VARIABLES =====")


class Employee2:
    raise_amount = 1.04  # class variable – shared by all instances
    num_employees = 0

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = f"{first}.{last}@company.com"
        Employee2.num_employees += 1

    def fullname(self):
        return f"{self.first} {self.last}"

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount)  # can access via instance or class


emp3 = Employee2("Alice", "Smith", 70000)
emp4 = Employee2("Bob", "Jones", 80000)

print(emp3.pay)  # 70000
emp3.apply_raise()
print(emp3.pay)  # 72800 (70000 * 1.04)
print(Employee2.raise_amount)  # 1.04
print(emp3.raise_amount)  # 1.04
print(Employee2.num_employees)  # 2

print("\n===== PART 3: CLASSMETHODS =====")


class Employee3:
    raise_amount = 1.04

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay

    @classmethod
    def set_raise_amount(cls, amount):
        cls.raise_amount = amount

    @classmethod
    def from_string(cls, emp_str):
        # Alternative constructor: parse "first-last-pay"
        first, last, pay = emp_str.split("-")
        return cls(first, last, int(pay))


emp5 = Employee3.from_string("John-Doe-90000")
print(emp5.pay)  # 90000
Employee3.set_raise_amount(1.05)
print(Employee3.raise_amount)  # 1.05

print("\n===== PART 4: STATICMETHODS =====")


class Employee4:
    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay

    @staticmethod
    def is_workday(day):
        # day is a datetime.date object
        return day.weekday() < 5  # Monday=0, Sunday=6


import datetime

my_date = datetime.date(2026, 6, 24)  # Wednesday
print(Employee4.is_workday(my_date))  # True
