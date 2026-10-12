import random


def make_question():
    symbol = random.choice(["+", "-", "*", "/"])

    if symbol == "/":
        number2 = random.randint(1, 12)
        answer = random.randint(1, 12)
        number1 = number2 * answer
    else:
        number1 = random.randint(1, 12)
        number2 = random.randint(1, 12)

        if symbol == "+":
            answer = number1 + number2
        elif symbol == "-":
            if number1 < number2:
                number1, number2 = number2, number1
            answer = number1 - number2
        else:
            answer = number1 * number2

    if random.choice([True, False]):
        question = f"? {symbol} {number2} = {answer}"
        correct_number = number1
    else:
        question = f"{number1} {symbol} ? = {answer}"
        correct_number = number2

    return question, correct_number


def play_game():
    print("Guess the missing number.")

    while True:
        question, correct_number = make_question()
        print(f"\n{question}")

        while True:
            try:
                guess = int(input("Your guess: "))
                break
            except ValueError:
                print("Please enter a whole number.")

        if guess == correct_number:
            print("Correct!")
        else:
            print(f"Not quite. The missing number was {correct_number}.")

        again = input("Play again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    play_game()
