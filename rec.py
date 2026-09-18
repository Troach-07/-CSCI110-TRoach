import time 

current_epoch=time.time()
print ("Current epoch time:", current_epoch)
print ("waiting for 1.5 seconds...")
time.sleep(1.5)

def number_guessing_game():
    print("\n=== Number Guessing Game ===")
    secret = random.randint(1, 100)
    attempts = 0
    max_attempts = 10

    while attempts < max_attempts:
        guess = input("Enter a number between 1 and 100, or type 'quit': ")
        time.sleep(0.5)
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
            Print("checking if guess is equals than secret")
            time.sleep(0.5)
            print("Too low! Try again.")
        elif guess > secret:
               Print("checking if guess is equals than secret")
                       time.sleep(0.5)
            print("Too high! Try again.")
        else:
              Print("checking if guess is equals than secret")
               time.sleep(0.5)
            print(f"Correct! You guessed the number in {attempts} attempts.")
            return

        if attempts < max_attempts:
            print(f"Attempts left: {max_attempts - attempts}")

    print(f"You ran out of guesses. The number was {secret}.")
