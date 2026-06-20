# Rock-Paper-Scissors
# First to 3 wins

import random

options = ["rock", "paper", "scissors"]
player_score = 0
computer_score = 0

print("Rock, Paper, Scissors — first to 3 wins!\n")

while player_score < 3 and computer_score < 3:
    player = input("Your choice (rock/paper/scissors): ").lower()
    
    if player not in options:
        print("Invalid choice, try again.")
        continue
    
    computer = random.choice(options)
    print(f"Computer chose: {computer}")
    
    if player == computer:
        print("It's a tie!")
    elif (player == "rock" and computer == "scissors") or \
         (player == "scissors" and computer == "paper") or \
         (player == "paper" and computer == "rock"):
        print("You win this round!")
        player_score += 1
    else:
        print("Computer wins this round!")
        computer_score += 1
    
    print(f"Score: You {player_score} - {computer_score} Computer\n")

if player_score == 3:
    print("You won the game!")
else:
    print("Computer won the game!")