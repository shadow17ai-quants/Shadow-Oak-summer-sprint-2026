# Day 2 - Conditionals, Loops, and Logic

# ============================================
# If Statements & Comparison Operators
# ============================================
temperature = 35
if temperature > 30:
    print("It's a hot day")
elif temperature > 20:
    print("It's a nice day")
elif temperature > 10:
    print("It's a cold day")
else:
    print("It's freezing")

points = 85
if points >= 90:
    print("Grade: A")
elif points >= 80:
    print("Grade: B")
elif points >= 70:
    print("Grade: C")
elif points >= 60:
    print("Grade: D")
else:
    print("Grade: F")

# ============================================
# Logical Operators
# ============================================
income = 60000
credit_score = 720
if income > 50000 and credit_score > 700:
    print("Loan approved")
elif income > 50000 or credit_score > 700:
    print("Further review needed")
else:
    print("Loan denied")

# Weight Converter
weight = float(input("Weight: "))
unit = input("(K)g or (L)bs: ")
if unit.upper() == "K":
    converted = weight * 2.20462
    print(f"{weight} kg = {converted:.2f} lbs")
elif unit.upper() == "L":
    converted = weight / 2.20462
    print(f"{weight} lbs = {converted:.2f} kg")
else:
    print("Invalid unit")

# ============================================
# While Loops
# ============================================
i = 1
while i <= 5:
    print(i)
    i += 1

# Guessing Game
secret = 9
guess_count = 0
guess_limit = 3
while guess_count < guess_limit:
    guess = int(input("Guess: "))
    guess_count += 1
    if guess == secret:
        print("You win!")
        break
else:
    print("You lose!")

# ============================================
# For Loops
# ============================================
for item in ["apple", "banana", "mango"]:
    print(item)

for number in range(5):
    print(number)

for number in range(2, 10, 2):
    print(number)

# ============================================
# Nested Loops
# ============================================
for x in range(4):
    for y in range(3):
        print(f"({x}, {y})")

# ============================================
# Car Game
# ============================================
command = ""
started = False
while True:
    command = input("> ").lower()
    if command == "start":
        if started:
            print("Car is already started!")
        else:
            started = True
            print("Car started...")
    elif command == "stop":
        if not started:
            print("Car is already stopped!")
        else:
            started = False
            print("Car stopped.")
    elif command == "help":
        print("""
start - to start the car
stop - to stop the car
quit - to exit
        """)
    elif command == "quit":
        break
    else:
        print("I don't understand that...")