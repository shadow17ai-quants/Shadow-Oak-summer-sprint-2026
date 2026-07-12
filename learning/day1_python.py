# Day 1 - Python Basics

# Variables - containers for storing data
age = 20  # integer
price = 19.95  # float
name = "Ryan"  # string
is_online = True  # boolean
print(age, price, name, is_online)

# Input & Type Conversion
# input() returns a string; int() converts to integer
birth_year = input("Enter your birth year: ")
age = 2026 - int(birth_year)
print(age)

# Strings - sequences of characters, indexed from 0
course = "Python for Beginners"
print(course[0])  # first character
print(course[-1])  # last character
print(course[0:3])  # slice from index 0 to 2

# Formatted Strings - embed variables/expressions inside strings
first = "Ryan"
last = "Kaushal"
msg = f"{first} {last} is learning Python"  # f-string
print(msg)

# String Methods - built-in functions that operate on strings
print(course.upper())  # all uppercase
print(course.lower())  # all lowercase
print(course.find("y"))  # index of first 'y' (-1 if not found)
print(course.replace("for", "4"))  # replace substring

# Arithmetic Operators
print(10 + 3)  # addition
print(10 / 3)  # division (float)
print(10 // 3)  # floor division (integer)
print(10 % 3)  # modulo (remainder)
print(10**3)  # exponent (10^3)

# Math Functions - from the math module
import math

print(round(2.9))  # round to nearest integer
print(abs(-2.9))  # absolute value
print(math.ceil(2.2))  # round up
print(math.floor(2.9))  # round down
