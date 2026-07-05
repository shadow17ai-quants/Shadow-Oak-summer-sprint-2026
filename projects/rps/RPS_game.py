# projects/rps/RPS_game.py
# Rock-Paper-Scissors – Day 2

import random

choices = ["rock", "paper", "scissors"]
score = {"win": 0, "loss": 0, "tie": 0}

while True:
    user = input("Enter rock, paper, scissors (or 'quit' to stop): ").lower()
    if user == "quit":
        break
    if user not in choices:
        print("Invalid choice. Try again.")
        continue

    computer = random.choice(choices)
    print(f"Computer chose: {computer}")

    if user == computer:
        result = "tie"
        score["tie"] += 1
        print("It's a tie!")
    elif (user == "rock" and computer == "scissors") or \
         (user == "scissors" and computer == "paper") or \
         (user == "paper" and computer == "rock"):
        result = "win"
        score["win"] += 1
        print("You win!")
    else:
        result = "loss"
        score["loss"] += 1
        print("You lose!")

print(f"\nFinal Score: {score['win']} wins, {score['loss']} losses, {score['tie']} ties")