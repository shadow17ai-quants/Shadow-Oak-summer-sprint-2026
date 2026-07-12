# language_python/day4_python.py – Dictionaries, Emoji Converter, Functions intro

print("===== DICTIONARIES =====")
# Key-value pairs – like a real-world dictionary
customer = {"name": "Ryan Kaushal", "age": 20, "is_verified": True}
print(customer["name"])  # Ryan Kaushal
print(customer.get("age"))  # 20
print(customer.get("birthdate"))  # None (doesn't crash)

# Update / add
customer["age"] = 21
customer["city"] = "Kharar"
print(
    customer
)  # {'name': 'Ryan Kaushal', 'age': 21, 'is_verified': True, 'city': 'Kharar'}

print("\n===== EMOJI CONVERTER (basic) =====")
# Map text emoticons to actual emojis
emoji_map = {":)": "😊", ":(": "😢", ":D": "😄", "<3": "❤️"}

message = input("Enter a message with emoticons (e.g. Hello :) ): ")
words = message.split(" ")
output = ""
for word in words:
    output += emoji_map.get(word, word) + " "
print("Converted:", output)

print("\n===== FUNCTIONS =====")


# 1. Basic function
def greet(name):
    return f"Hello, {name}!"


print(greet("Ryan"))  # Hello, Ryan!


# 2. Multiple parameters
def add(a, b):
    return a + b


print(add(5, 3))  # 8


# 3. Default parameter
def power(base, exponent=2):
    return base**exponent


print(power(3))  # 9  (3^2)
print(power(3, 3))  # 27 (3^3)


# 4. *args – variable number of positional arguments
def sum_all(*args):
    total = 0
    for num in args:
        total += num
    return total


print(sum_all(1, 2, 3, 4, 5))  # 15


# 5. **kwargs – variable number of keyword arguments
def print_person(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")


print_person(
    name="Ryan",
    age=20,
)
# Output:
# name: Ryan
# age: 20


# 6. Scope – local vs global
x = 10  # global


def change_x():
    global x
    x = 20  # modifies global


change_x()
print(x)  # 20
