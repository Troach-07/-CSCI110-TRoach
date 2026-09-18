import random
import time 

SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
VALUES = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
FACE_CARDS = {11: "Jack", 12: "Queen", 13: "King", 14: "Ace"}
POKER_RANK_NAMES = {11: "Jack", 12: "Queen", 13: "King", 14: "Ace"}


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

        guess = input("Enter a letter or type 'quit' or 'solve': ").strip().lower()

        if guess == "quit":
            print("Thanks for playing! The word was:", word)
            return
        if guess == "solve":
            print "what is word?"
            

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter one letter only.")
            continue
        if guess == word:
            print("Congratulations! You guessed the whole word!")
            return

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
        print "Pick Your Game"
        play=input("Pick Your Game")

       
        if play == "Poker" 
    def poker_card_name(card):
    value = card["value"]
    if value in POKER_RANK_NAMES:
        value_name = POKER_RANK_NAMES[value]
    else:
        value_name = str(value)
    return f"{value_name} of {card['suit']}"


def poker_score_hand(hand):
    values = sorted(card["value"] for card in hand)
    counts = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1

    is_flush = len({card["suit"] for card in hand}) == 1
    is_straight = False
    if values == [2, 3, 4, 5, 14]:
        is_straight = True
        values = [1, 2, 3, 4, 5]
    elif values[0] + 4 == values[4]:
        is_straight = True

    counts_list = sorted(counts.values(), reverse=True)

    if is_flush and is_straight:
        return 8, values[-1]
    if counts_list == [4, 1]:
        return 7, max(counts)
    if counts_list == [3, 2]:
        return 6, max(counts)
    if is_flush:
        return 5, values[-1]
    if is_straight:
        return 4, values[-1]
    if counts_list == [3, 1, 1]:
        return 3, max(counts)
    if counts_list == [2, 2, 1]:
        return 2, sorted(counts, key=lambda v: (-counts[v], -v))[0]
    if counts_list == [2, 1, 1, 1]:
        return 1, sorted(counts, key=lambda v: (-counts[v], -v))[0]
    return 0, max(values)


def poker_hand_rank_name(rank_number):
    names = {
        8: "Straight Flush",
        7: "Four of a Kind",
        6: "Full House",
        5: "Flush",
        4: "Straight",
        3: "Three of a Kind",
        2: "Two Pair",
        1: "One Pair",
        0: "High Card",
    }
    return names[rank_number]


def poker_game():
    print("\n=== Poker ===")
    print("You are dealt 5 cards. The best hand wins.")
    deck = create_deck()
    hand = [deck.pop() for _ in range(5)]
    print("\nYour hand:")
    for card in hand:
        print("-", poker_card_name(card))

    rank, tiebreak = poker_score_hand(hand)
    print("Hand ranking:", poker_hand_rank_name(rank))
    print("Tiebreak value:", tiebreak)
    return 


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


def create_deck():
    deck = []
    for suit in SUITS:
        for value in VALUES:
            deck.append({"suit": suit, "value": value})
    random.shuffle(deck)
    return deck


def blackjack_card_name(card):
    value = card["value"]
    if value in FACE_CARDS:
        name = FACE_CARDS[value]
    else:
        name = str(value)
    return f"{name} of {card['suit']}"


def hand_total(hand):
    total = 0
    aces = 0

    for card in hand:
        value = card["value"]
        if value == 14:
            aces += 1
            total += 11
        else:
            total += min(value, 10)

    while total > 21 and aces > 0:
        total -= 10
        aces -= 1

    return total


def deal_card(deck):
    return deck.pop()


def show_hand(name, hand):
    print(f"{name}'s hand:")
    for card in hand:
        print("  -", blackjack_card_name(card))
    print("Total:", hand_total(hand))


def blackjack_game():
    print("\n=== Blackjack ===")
    deck = create_deck()
    player_hand = [deal_card(deck), deal_card(deck)]
    dealer_hand = [deal_card(deck), deal_card(deck)]

    while True:
        show_hand("Player", player_hand)
        print("Dealer shows:", blackjack_card_name(dealer_hand[0]))

        if hand_total(player_hand) == 21:
            print("You hit 21! You win!")
            return

        if hand_total(player_hand) > 21:
            print("You busted! Dealer wins.")
            return

        choice = input("Do you want to hit or stand? (h/s): ").strip().lower()

        if choice == "h":
            player_hand.append(deal_card(deck))
        elif choice == "s":
            break
        else:
            print("Please enter 'h' for hit or 's' for stand.")

    print("\nDealer's turn:")
    show_hand("Dealer", dealer_hand)

    while hand_total(dealer_hand) < 17:
        dealer_hand.append(deal_card(deck))
        print("Dealer hits:")
        show_hand("Dealer", dealer_hand)

    player_total = hand_total(player_hand)
    dealer_total = hand_total(dealer_hand)

    print("\nFinal results:")
    show_hand("Player", player_hand)
    show_hand("Dealer", dealer_hand)

    if dealer_total > 21:
        print("Dealer busted! You win!")
    elif player_total > dealer_total:
        print("You win!")
    elif player_total < dealer_total:
        print("Dealer wins!")
    else:
        print("It's a tie!")




def show_menu():
    print("\nWelcome to the Game Center!")
    print("1. Number Guessing")
    print("2. Hangman")
    print("3. Rock Paper Scissors")
    print("4. Dice Guessing")
    print("5. Gambling")
    print("6. Blackjack")
    print("7. Poker")
    print("8. Exit")


while True:
    show_menu()
    choice = input("Choose a game (1-8): ").strip()

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
        blackjack_game()
    elif choice == "7":
        poker_game()
    elif choice == "8":
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please choose 1 through 8.")