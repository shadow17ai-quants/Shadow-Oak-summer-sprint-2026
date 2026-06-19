# Day 1 - Python Basics

# Variables
age = 20
price = 19.95
name = "Ryan"
is_online = True
print(age, price, name, is_online)

# Input & Type Conversion
birth_year = input("Enter your birth year: ")
age = 2026 - int(birth_year)
print(age)

# Strings
course = "Python for Beginners"
print(course[0])
print(course[-1])
print(course[0:3])

# Formatted Strings
first = "Ryan"
last = "Kaushal"
msg = f"{first} {last} is learning Python"
print(msg)

# String Methods
print(course.upper())
print(course.lower())
print(course.find("y"))
print(course.replace("for", "4"))

# Arithmetic
print(10 + 3)
print(10 / 3)
print(10 // 3)
print(10 % 3)
print(10 ** 3)

# Math Functions
import math
print(round(2.9))
print(abs(-2.9))
print(math.ceil(2.2))
print(math.floor(2.9))