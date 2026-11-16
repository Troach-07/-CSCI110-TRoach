import random


def number_guessing_game():
    print("\n=== Number Guessing Game ===")
    secret = random.randint(1, 100)
    attempts = 0
    max_attempts = 10

    while attempts < max_attempts:
        guess = input("Enter a number between 1 and 100, or type 'quit': ")
        if guess.lower() == "quit":
            print("Thanks for playing!")
            return

        try:
            guess = int(guess)
        except ValueError:
            print("Please enter a valid number.")
            continue

        attempts += 1

        if guess < secret:
            print("Too low! Try again.")
        elif guess > secret:
            print("Too high! Try again.")
        else:
            print(f"Correct! You guessed the number in {attempts} attempts.")
            return

        if attempts < max_attempts:
            print(f"Attempts left: {max_attempts - attempts}")

    print(f"You ran out of guesses. The number was {secret}.")


def hangman_game():
    print("\n=== Hangman ===")
    words = [
        "python", "computer", "hangman", "student", "programming", "keyboard",
        "library", "science", "challenge", "coffee", "teacher", "window",
        "planet", "rocket", "diamond", "garden", "forest", "ocean", "mountain",
        "pencil", "notebook", "holiday", "sunshine", "rainbow", "basketball",
        "soccer", "baseball", "bicycle", "universe", "language", "history",
        "mathematics", "friendship", "adventure", "campfire", "backpack",
        "journey", "picture", "morning", "evening", "machine", "browser",
        "internet", "software", "hardware", "database", "memory", "learning",
        "festival", "camera", "message", "airplane", "castle", "butterfly",
        "puzzle", "village", "harbor", "bridge", "musical", "concert",
        "guitar", "piano", "victory", "orange", "banana", "strawberry",
        "pineapple", "tomato", "potato", "sandwich", "pizza", "burger"
    ]

    word = random.choice(words)
    guessed_letters = []
    wrong_guesses = 0
    max_wrong = 6

    hangman = [
        """
      +---+
      |   |
          |
          |
          |
          |
    ========== 
        """,
        """
      +---+
      |   |
      O   |
          |
          |
          |
    ========== 
        """,
        """
      +---+
      |   |
      O   |
      |   |
          |
          |
    ========== 
        """,
        """
      +---+
      |   |
      O   |
     /|   |
          |
          |
    ========== 
        """,
        """
      +---+
      |   |
      O   |
     /|\\  |
          |
          |
    ========== 
        """,
        """
      +---+
      |   |
      O   |
     /|\\  |
     /    |
          |
    ========== 
        """,
        """
      +---+
      |   |
      O   |
     /|\\  |
     / \\ |
          |
    ========== 
        """
    ]

    while wrong_guesses < max_wrong:
        display = ""
        for letter in word:
            if letter in guessed_letters:
                display += letter + " "
            else:
                display += "_ "

        print("\n" + hangman[wrong_guesses])
        print("Word:", display)
        print("Guessed letters:", " ".join(guessed_letters) if guessed_letters else "None")

        guess = input("Enter a letter or type 'quit': ").strip().lower()

        if guess == "quit":
            print("Thanks for playing! The word was:", word)
            return

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter one letter only.")
            continue

        if guess in guessed_letters:
            print("You already guessed that letter.")
            continue

        guessed_letters.append(guess)

        if guess in word:
            print("Correct!")
        else:
            wrong_guesses += 1
            print("Incorrect! That letter is not in the word.")

        if all(letter in guessed_letters for letter in set(word)):
            print("\nYou win! The word was:", word)
            return

    print("\n" + hangman[max_wrong])
    print("You ran out of guesses! The word was:", word)


def rock_paper_scissors_game():
    print("\n=== Rock, Paper, Scissors ===")
    choices = ["rock", "paper", "scissors"]
    user_score = 0
    computer_score = 0

    while True:
        print(f"\nScore: You {user_score} - Computer {computer_score}")
        user_choice = input("Choose rock, paper, scissors, or quit: ").strip().lower()

        if user_choice == "quit":
            print("Final score:", f"You {user_score} - Computer {computer_score}")
            return

        if user_choice not in choices:
            print("Please choose rock, paper, or scissors.")
            continue

        computer_choice = random.choice(choices)
        print("Computer chose:", computer_choice)

        if user_choice == computer_choice:
            print("It's a tie!")
        elif (
            (user_choice == "rock" and computer_choice == "scissors") or
            (user_choice == "paper" and computer_choice == "rock") or
            (user_choice == "scissors" and computer_choice == "paper")
        ):
            user_score += 1
            print("You win this round!")
        else:
            computer_score += 1
            print("Computer wins this round!")


def dice_game():
    print("\n=== Dice Guessing Game ===")
    while True:
        guess = input("Guess the dice roll (1-6) or type 'quit': ")
        if guess.lower() == "quit":
            print("Thanks for playing!")
            return

        try:
            guess = int(guess)
        except ValueError:
            print("Please enter a number from 1 to 6.")
            continue

        if guess < 1 or guess > 6:
            print("Your guess must be between 1 and 6.")
            continue

        roll = random.randint(1, 6)
        print("The die rolled a", roll)

        if guess == roll:
            print("You guessed correctly!")
        else:
            print("Not quite. Try again!")


def gambling_game():
    print("\n=== Gambling Game ===")
    print("You start with $50.")
    money = 50

    while True:
        print(f"\nCurrent money: ${money}")
        bet = input("Enter your bet amount or type 'quit': ")

        if bet.lower() == "quit":
            print("Thanks for playing! Final money:", money)
            return

        try:
            bet = int(bet)
        except ValueError:
            print("Please enter a valid number.")
            continue

        if bet <= 0:
            print("Bet must be greater than 0.")
            continue

        if bet > money:
            print("You cannot bet more than you have.")
            continue

        roll = random.randint(1, 6)
        guess = input("Choose a number from 1 to 6: ")

        try:
            guess = int(guess)
        except ValueError:
            print("Please enter a valid number from 1 to 6.")
            continue

        if guess < 1 or guess > 6:
            print("Your guess must be between 1 and 6.")
            continue

        print("The dice rolled a", roll)

        if guess == roll:
            money += bet * 2
            print("You win! You doubled your bet.")
        else:
            money -= bet
            print("You lose this round.")

        if money <= 0:
            print("You are out of money. Game over!")
            return


def show_menu():
    print("Welcome to the Game Center!")
    print("1. Number Guessing")
    print("2. Hangman")
    print("3. Rock Paper Scissors")
    print("4. Dice Guessing")
    print("5. Gambling")
    print("6. Exit")


while True:
    show_menu()
    choice = input("Choose a game (1-6): ").strip()

    if choice == "1":
        number_guessing_game()
    elif choice == "2":
        hangman_game()
    elif choice == "3":
        rock_paper_scissors_game()
    elif choice == "4":
        dice_game()
    elif choice == "5":
        gambling_game()
    elif choice == "6":
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please choose 1, 2, 3, 4, 5, or 6.")
