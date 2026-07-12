# language_python/day5_python.py – Exceptions (try/except/else/finally)

print("===== EXCEPTIONS =====")

# Basic try/except
try:
    age = int(input("Enter your age: "))
    print(f"Your age is {age}")
except ValueError:
    print("That's not a valid number!")

print("\n===== TRY / EXCEPT / ELSE =====")

try:
    num = int(input("Enter a number: "))
except ValueError:
    print("Invalid input!")
else:
    # Runs only if no exception occurred
    print(f"Perfect! You entered {num}")
finally:
    # Always runs – good for cleanup (closing files, DB connections)
    print("This always executes.")

print("\n===== HANDLING MULTIPLE EXCEPTIONS =====")

try:
    result = 10 / int(input("Enter a divisor: "))
    print(f"10 / divisor = {result}")
except ZeroDivisionError:
    print("Cannot divide by zero!")
except ValueError:
    print("Please enter a valid integer!")
except Exception as e:
    print(f"Something else went wrong: {e}")

print("\n===== RAISING EXCEPTIONS =====")


def check_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative!")
    print(f"Age is {age}")


try:
    check_age(-5)
except ValueError as e:
    print(f"Caught an error: {e}")

print("\n===== FILE I/O WITH EXCEPTIONS =====")
# Practical use: reading a file that might not exist
try:
    with open("nonexistent.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    print("File not found! Creating a new one.")
    with open("nonexistent.txt", "w") as f:
        f.write("Created by exception handler.")
