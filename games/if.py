# int num
import random

num = random.randint(1, 1000)
guess_count = 0
while True:
    guess = input("Enter your guess (or type stop): ")
    if guess.lower() == "stop":
        print("Game stopped by user.")
        print("Thank you for playing!")
        print("The correct number was:", num)
        print("Number of guesses:", guess_count)
        break

    try:
        guess = int(guess)
    except ValueError:
        print("Please enter a number or type stop.")
        continue

    if guess_count == 10:
        print("You have exceeded the maximum number of guesses (10).")
        print("The correct number was:", num)
        print("Thank you for playing!")
        break

    guess_count += 1
    print("guess number")
    if guess == num:
        print("Correct!")
        print("Thank you for playing!")
        print("Number of guesses:", guess_count)
        break
    else:
        print("Incorrect!")
        if guess < num:
            print(guess, "-is too low.")
            print(f"Guess again! You have {10 - guess_count} guesses left.")
        if guess > num:
            print(guess, "-is too high.")
            print(f"Guess again! You have {10 - guess_count} guesses left.")
        print("Guess again!")


