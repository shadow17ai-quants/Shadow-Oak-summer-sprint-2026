# Day 2 - Conditionals & Loops

# ============================================
# If Statements
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

# ============================================
# Comparison Operators
# >, >=, <, <=, ==, !=
# ============================================
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
# Logical Operators (and, or, not)
# ============================================
income = 60000
credit_score = 720

if income > 50000 and credit_score > 700:
    print("Loan approved")
elif income > 50000 or credit_score > 700:
    print("Further review needed")
else:
    print("Loan denied")

# ============================================
# Weight Converter Program
# ============================================
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