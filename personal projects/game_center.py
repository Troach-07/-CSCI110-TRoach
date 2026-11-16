import math
import random
import sys
import time 

SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
VALUES = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
FACE_CARDS = {11: "Jack", 12: "Queen", 13: "King", 14: "Ace"}
POKER_RANK_NAMES = {11: "Jack", 12: "Queen", 13: "King", 14: "Ace"}

##How the Money Formatting Works
def format_balance(amount):
    if amount >= 1_000_000_000:
        scaled_amount = amount / 1_000_000_000
        suffix = "b"
    elif amount >= 1_000_000:
        scaled_amount = amount / 1_000_000
        suffix = "m"
    elif amount >= 1_000:
        scaled_amount = amount / 1_000
        suffix = "k"
    else:
        return str(amount)

    rounded_amount = f"{scaled_amount:.1f}".rstrip("0").rstrip(".")
    return f"{rounded_amount}{suffix}"

##How the money valuing works
def parse_money(value):
    value = value.strip().lower().replace("$", "")
    multipliers = {"k": 1_000, "m": 1_000_000, "b": 1_000_000_000}

    if not value:
        raise ValueError

    multiplier = 1
    if value[-1] in multipliers:
        multiplier = multipliers[value[-1]]
        value = value[:-1]

    amount = float(value) * multiplier
    if amount != int(amount):
        raise ValueError
    return int(amount)

## How to get the bet amount
def get_bet(money):
    while True:
        bet = input("Enter your bet amount or type 'quit': ").strip()
        if bet.lower() == "quit":
            return None

        try:
            bet = parse_money(bet)
        except ValueError:
            print("Please enter a valid amount, such as 500, 1k, 2.5m, or 1b.")
            continue

        if bet <= 0:
            print("Bet must be greater than 0.")
        elif bet > money:
            print("You cannot bet more than you have.")
        else:
            return bet


def number_guessing_game(money=None, bet=0):
    gambling = money is not None
    print("\n=== Number Guessing Game ===")
    secret = random.randint(1, 100)
    attempts = 0
    max_attempts = 10
    ## how many tries the player has to guess the number between 1 and 100
    while attempts < max_attempts:
        guess = input("Enter a number between 1 and 100, or type 'quit': ")
        time.sleep(0.5)
        if guess.lower() == "quit":
            print("Thanks for playing!")
            return money if gambling else None

        try:
            guess = int(guess)
        except ValueError:
            ## Check if the input is a valid number
            print("Please enter a valid number.")
            continue
        ## if the attempt is valid it adds to the attempt count 
        attempts += 1

        if guess < secret:
            print("checking if guess is equal to the secret")
            time.sleep(0.5)
            print("Too low! Try again.")
        elif guess > secret:
            print("checking if guess is equal to the secret")
            time.sleep(0.5)
            print("Too high! Try again.")
        else:
            print("checking if guess is equal to the secret")
            time.sleep(0.5)
            print(f"Correct! You guessed the number in {attempts} attempts.")
            return money + bet if gambling else None

        if attempts < max_attempts:
            print(f"Attempts left: {max_attempts - attempts}")

    print(f"You ran out of guesses. The number was {secret}.")
    return money - bet if gambling else None


def hangman_game(money=None, bet=0):
    gambling = money is not None
    print("\n=== Hangman ===")
    ## List of words for the game
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
    ## Pick a random word from the list above 
    word = random.choice(words)
    guessed_letters = []
    wrong_guesses = 0
    max_wrong = 6
    ## for each wrong guess, display a part of the hangman
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
    ## Main game loop 
    while wrong_guesses < max_wrong:
        display = ""
        for letter in word:
            if letter in guessed_letters:
                display += letter + " "
            else:
                display += "_ "
        ## this displays the hangman and the current state of the word
        print("\n" + hangman[wrong_guesses])
        print("Word:", display)
        print("Guessed letters:", " ".join(guessed_letters) if guessed_letters else "None")

        guess = input("Enter a letter or type 'quit' or 'solve': ").strip().lower()
        print("picking a word...")
        time.sleep(0.5)
        print("word picked")
        ##if you want to quit the game it tells you the word and returns the money
        if guess == "quit":
            print("Thanks for playing! The word was:", word)
            return money if gambling else None
        if guess == "solve":
            time.sleep(0.5)
            print("what is word?")

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter one letter only.")
            continue
        if guess == word:
            ##check if guess is equal to the secret word if it is you win if not you lose
            print("checking if guess is equal to the secret")
            time.sleep(0.5)
            print("Congratulations! You guessed the whole word!")
            return money + bet if gambling else None
        ##prevents you from guessing the same letter twice
        if guess in guessed_letters:
            print("You already guessed that letter.")
            continue

        guessed_letters.append(guess)
    ##check if the guessed letter is in the word
        if guess in word:
            print("checking if letter is in the word")
            time.sleep(0.5)
            print("Correct!")
        else:
            wrong_guesses += 1
            print("Incorrect! That letter is not in the word.")

        if all(letter in guessed_letters for letter in set(word)):
            print("checking if letter is in the word")
            time.sleep(0.5)
            print("\nYou win! The word was:", word)
            return money + bet if gambling else None
    ##for if you run out of guesses an lose the game
    print("\n" + hangman[max_wrong])
    print("You ran out of guesses! The word was:", word)
    return money - bet if gambling else None


def rock_paper_scissors_game(money=None, bet=0):
    ## Determine if the game is being played with money
    gambling = money is not None
    print("\n=== Rock, Paper, Scissors ===")
    choices = ["rock", "paper", "scissors"]
    user_score = 0
    computer_score = 0

    while True:
        ## Display the current score and pick rock paper scissors
        print(f"\nScore: You {user_score} - Computer {computer_score}")
        user_choice = input("Choose rock, paper, scissors, or quit: ").strip().lower()

        if user_choice == "quit":
            print("Final score:", f"You {user_score} - Computer {computer_score}")
            return money if gambling else None

        if user_choice not in choices:
            print("Please choose rock, paper, or scissors.")
            continue

        computer_choice = random.choice(choices)
        print("Computer chose:", computer_choice)
        ##tells you if you won or lost
        if user_choice == computer_choice:
            print("It's a tie!")
            if gambling:
                return money
        elif (
            (user_choice == "rock" and computer_choice == "scissors") or
            (user_choice == "paper" and computer_choice == "rock") or
            (user_choice == "scissors" and computer_choice == "paper")
        ):
            user_score += 1
            print("You win this round!")
            if gambling:
                return money + (2*bet)
        else:
            computer_score += 1
            print("Computer wins this round!")
            if gambling:
                return money - bet


def dice_game():
    ##Roll the dice and guess the outcome if right win money
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
        print("Rolling the dice...")
        time.sleep(0.5)
        print("The die rolled a", roll)

        if guess == roll:
            print("You guessed correctly!")
        else:
            print("Not quite. Try again!")


def multiplication_game():
    ##Secret Money Solutions 
    ##adds money to the player's balance
    print("\n=== Starting Balance ===")
    try:
        amount_to_add = parse_money(input("Enter the amount of money you want to add: "))
        current_money_input = input("Enter the amount of money you want to play with (default 50): ").strip()
        current_money = parse_money(current_money_input) if current_money_input else 50
    except ValueError:
        print("Please enter valid amounts, such as 500, 1k, 2.5m, or 1b.")
        return None

    new_balance = current_money + amount_to_add
    print(f"Current balance: ${format_balance(current_money)}")
    print(f"New gambling balance: ${format_balance(new_balance)}")
    return new_balance


def field_finder_game():
    import subprocess
    import sys
    from pathlib import Path

    game_script = Path(__file__).resolve().parents[1] / "test.py"
    subprocess.run([sys.executable, str(game_script)], check=False)


def render_roulette_wheel(ball_position):
    width = 31
    height = 15
    center_x = (width - 1) / 2
    center_y = (height - 1) / 2
    lines = []

    for row in range(height):
        cells = []
        for column in range(width):
            x = (column - center_x) / 14
            y = (row - center_y) / 6.5
            radius = math.hypot(x, y)
            if 0.75 <= radius <= 1.08:
                angle = math.atan2(y, x)
                section = int((angle + math.pi) * 12 / (2 * math.pi)) % 12
                if section == ball_position:
                    cells.append("\033[43;97m* \033[0m")
                else:
                    color_code = 41 if section % 2 == 0 else 40
                    cells.append(f"\033[{color_code}m  \033[0m")
            elif row == int(center_y) and 11 <= column <= 18:
                label = "ROULETTE"
                cells.append(f"\033[1;37m{label[column - 11]} \033[0m")
            else:
                cells.append("  ")
        lines.append("".join(cells).rstrip())
    return "\n".join(lines)


def open_roulette_wheel(bet_type, bet_number, winning_number):
    import tempfile
    import webbrowser
    from pathlib import Path

    center = 450
    pocket_inner = 230
    pocket_outer = 340
    pocket_numbers = [
        0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23,
        10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26,
    ]
    winning_index = pocket_numbers.index(winning_number)
    wheel_rotation = 360 * 8 - winning_index * 360 / len(pocket_numbers)
    red_numbers = {
        1, 3, 5, 7, 9, 12, 14, 16, 18,
        19, 21, 23, 25, 27, 30, 32, 34, 36,
    }
    winning_color = "green" if winning_number == 0 else "red" if winning_number in red_numbers else "black"
    winning_swatch = {"green": "#167447", "red": "#bd2637", "black": "#17191a"}[winning_color]
    winning_detail = "ZERO" if winning_number == 0 else (
        f"{'EVEN' if winning_number % 2 == 0 else 'ODD'} · "
        f"{'LOW' if winning_number <= 18 else 'HIGH'}"
    )
    pockets = []
    slot_angle = 2 * math.pi / len(pocket_numbers)

    for index, number in enumerate(pocket_numbers):
        start_angle = -math.pi / 2 + index * slot_angle + 0.003
        end_angle = -math.pi / 2 + (index + 1) * slot_angle - 0.003
        middle_angle = (start_angle + end_angle) / 2
        outer_start = (
            center + pocket_outer * math.cos(start_angle),
            center + pocket_outer * math.sin(start_angle),
        )
        outer_end = (
            center + pocket_outer * math.cos(end_angle),
            center + pocket_outer * math.sin(end_angle),
        )
        inner_end = (
            center + pocket_inner * math.cos(end_angle),
            center + pocket_inner * math.sin(end_angle),
        )
        inner_start = (
            center + pocket_inner * math.cos(start_angle),
            center + pocket_inner * math.sin(start_angle),
        )
        color = "#167447" if number == 0 else "#bd2637" if number in red_numbers else "#17191a"
        pockets.append(
            f'<path d="M {outer_start[0]:.2f} {outer_start[1]:.2f} '
            f'A {pocket_outer} {pocket_outer} 0 0 1 {outer_end[0]:.2f} {outer_end[1]:.2f} '
            f'L {inner_end[0]:.2f} {inner_end[1]:.2f} '
            f'A {pocket_inner} {pocket_inner} 0 0 0 {inner_start[0]:.2f} {inner_start[1]:.2f} Z" '
            f'fill="{color}" stroke="#d4b76e" stroke-width="1.4"/>'
        )

        label_radius = 285
        label_x = center + label_radius * math.cos(middle_angle)
        label_y = center + label_radius * math.sin(middle_angle)
        label_rotation = math.degrees(middle_angle) + 90
        pockets.append(
            f'<text x="{label_x:.2f}" y="{label_y:.2f}" '
            f'transform="rotate({label_rotation:.2f} {label_x:.2f} {label_y:.2f})" '
            f'fill="#fff8e8" font-family="Georgia,serif" font-size="18" '
            f'font-weight="700" text-anchor="middle" dominant-baseline="middle">{number}</text>'
        )

    rim_bolts = []
    for index in range(16):
        angle = 2 * math.pi * index / 16
        bolt_x = center + 375 * math.cos(angle)
        bolt_y = center + 375 * math.sin(angle)
        rim_bolts.append(
            f'<circle cx="{bolt_x:.2f}" cy="{bolt_y:.2f}" r="5" '
            'fill="#f0d58b" stroke="#72552a" stroke-width="2"/>'
        )

    number_cells = []
    zero_stroke = "#ffe08a" if bet_type == "number" and bet_number == 0 else "#d4b76e"
    zero_width = 4 if bet_type == "number" and bet_number == 0 else 1.5
    number_cells.append(
        f'<rect x="930" y="132" width="424" height="38" rx="4" '
        f'fill="#167447" stroke="{zero_stroke}" stroke-width="{zero_width}"/>'
        '<text x="1142" y="157" fill="#fff8e8" font-family="Georgia,serif" '
        'font-size="18" font-weight="700" text-anchor="middle">0</text>'
    )
    if bet_type == "number" and bet_number == 0:
        number_cells.append('<path d="M 918 145 l 8 -6 v 12 Z" fill="#ffe08a"/>')
    if winning_number == 0:
        number_cells.append(
            '<rect id="winning-cell-highlight" x="930" y="132" width="424" height="38" '
            'rx="4" fill="none" stroke="#fff0a6" stroke-width="4"/>'
        )

    for number in range(1, 37):
        row, column = divmod(number - 1, 12)
        cell_x = 930 + column * 35
        cell_y = 181 + row * 49
        color = "#bd2637" if number in red_numbers else "#17191a"
        selected = bet_type == "number" and bet_number == number
        stroke = "#ffe08a" if selected else "#c9ad6a"
        stroke_width = 4 if selected else 1.5
        number_cells.append(
            f'<rect x="{cell_x}" y="{cell_y}" width="33" height="44" rx="3" '
            f'fill="{color}" stroke="{stroke}" stroke-width="{stroke_width}"/>'
            f'<text x="{cell_x + 16.5}" y="{cell_y + 28}" fill="#fff8e8" '
            'font-family="Georgia,serif" font-size="15" font-weight="700" '
            f'text-anchor="middle">{number}</text>'
        )
        if selected:
            number_cells.append(
                f'<path d="M {cell_x - 11} {cell_y + 22} l 8 -6 v 12 Z" fill="#ffe08a"/>'
            )
        if number == winning_number:
            number_cells.append(
                f'<rect id="winning-cell-highlight" x="{cell_x}" y="{cell_y}" '
                'width="33" height="44" rx="3" fill="none" '
                'stroke="#fff0a6" stroke-width="4"/>'
            )

    bet_options = [
        ("number", "Straight number", "#9a7540"),
        ("red", "Red", "#bd2637"),
        ("black", "Black", "#17191a"),
        ("even", "Even", "#ddd5c3"),
        ("odd", "Odd", "#ddd5c3"),
        ("low", "Low · 1 to 18", "#527b61"),
        ("high", "High · 19 to 36", "#527b61"),
    ]
    option_rows = []
    for index, (option, label, swatch) in enumerate(bet_options):
        option_y = 353 + index * 49
        selected = bet_type == option
        stroke = "#ffe08a" if selected else "#786443"
        stroke_width = 3 if selected else 1
        option_rows.append(
            f'<rect x="930" y="{option_y}" width="424" height="40" rx="4" '
            f'fill="#192820" stroke="{stroke}" stroke-width="{stroke_width}"/>'
            f'<rect x="944" y="{option_y + 8}" width="24" height="24" rx="3" '
            f'fill="{swatch}" stroke="#d4b76e" stroke-width="1"/>'
            f'<text x="984" y="{option_y + 26}" fill="#f8f1e1" '
            'font-family="Georgia,serif" font-size="17">'
            f'{label}{f" · {bet_number}" if option == "number" and bet_number is not None else ""}</text>'
        )
        if selected:
            option_rows.append(
                f'<path d="M 918 {option_y + 20} l 8 -6 v 12 Z" fill="#ffe08a"/>'
            )

    ball_x = center + 310 * math.cos(-math.pi / 2)
    ball_y = center + 310 * math.sin(-math.pi / 2)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="900" viewBox="0 0 1400 900">
<defs>
  <radialGradient id="table" cx="50%" cy="42%" r="70%">
    <stop offset="0" stop-color="#245743"/>
    <stop offset="1" stop-color="#102b22"/>
  </radialGradient>
  <radialGradient id="hub" cx="42%" cy="35%" r="70%">
    <stop offset="0" stop-color="#6b5030"/>
    <stop offset="1" stop-color="#29221b"/>
  </radialGradient>
  <filter id="shadow" x="-30%" y="-30%" width="160%" height="160%">
    <feDropShadow dx="0" dy="8" stdDeviation="9" flood-color="#000000" flood-opacity="0.5"/>
  </filter>
    <style>
        @keyframes wheel-spin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate({wheel_rotation:.2f}deg); }} }}
        @keyframes ball-spin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(-2880deg); }} }}
        #wheel-spin, #ball-spin {{ transform-box: view-box; transform-origin: 450px 450px; }}
        #wheel-spin {{ animation: wheel-spin 6s cubic-bezier(.12,.78,.18,1) forwards; }}
        #ball-spin {{ animation: ball-spin 6s cubic-bezier(.12,.78,.18,1) forwards; }}
        @keyframes reveal-result {{ 0%, 92% {{ opacity: 0; }} 100% {{ opacity: 1; }} }}
        @keyframes hide-spin {{ 0%, 92% {{ opacity: 1; }} 100% {{ opacity: 0; }} }}
        #winner-display, #winning-cell-highlight {{ opacity: 0; animation: reveal-result 6s linear forwards; }}
        #spin-display {{ animation: hide-spin 6s linear forwards; }}
        @media (prefers-reduced-motion: reduce) {{
            #wheel-spin {{ animation: none; transform: rotate({wheel_rotation:.2f}deg); }}
            #ball-spin {{ animation: none; transform: rotate(-2880deg); }}
            #winner-display, #winning-cell-highlight {{ animation: none; opacity: 1; }}
            #spin-display {{ display: none; }}
        }}
    </style>
</defs>
<rect width="1400" height="900" fill="url(#table)"/>
<g id="wheel-spin">
<circle cx="450" cy="450" r="415" fill="#171817" stroke="#9b753d" stroke-width="14" filter="url(#shadow)"/>
<circle cx="450" cy="450" r="395" fill="#302619" stroke="#e1c477" stroke-width="5"/>
<circle cx="450" cy="450" r="371" fill="#17191a" stroke="#745832" stroke-width="8"/>
{''.join(pockets)}
<circle cx="450" cy="450" r="343" fill="none" stroke="#f0d58b" stroke-width="5"/>
<circle cx="450" cy="450" r="229" fill="#bd9852" stroke="#f0d58b" stroke-width="5"/>
<circle cx="450" cy="450" r="218" fill="url(#hub)" stroke="#35291a" stroke-width="5"/>
<circle cx="450" cy="450" r="177" fill="none" stroke="#ad8546" stroke-width="3"/>
<circle cx="450" cy="450" r="165" fill="#17241e" stroke="#e0c276" stroke-width="4"/>
<circle cx="450" cy="450" r="145" fill="url(#hub)" stroke="#806137" stroke-width="3"/>
<path d="M 450 275 L 435 247 L 450 210 L 465 247 Z" fill="#dfc276" stroke="#49371e" stroke-width="4"/>
<text x="450" y="427" fill="#e4cb8c" font-family="Georgia,serif" font-size="19" letter-spacing="4" text-anchor="middle">SINGLE ZERO</text>
<text x="450" y="468" fill="#fff5dc" font-family="Georgia,serif" font-size="32" font-weight="700" text-anchor="middle">ROULETTE</text>
<text x="450" y="500" fill="#c7aa69" font-family="Georgia,serif" font-size="15" letter-spacing="3" text-anchor="middle">EST. 1895</text>
{''.join(rim_bolts)}
</g>
<g id="ball-spin">
<circle cx="{ball_x:.2f}" cy="{ball_y:.2f}" r="13" fill="#fffdf4" stroke="#8a7853" stroke-width="4" filter="url(#shadow)"/>
</g>
<path d="M 450 17 L 435 51 L 465 51 Z" fill="#f6e3a7" stroke="#4b3a20" stroke-width="4"/>
<path d="M 900 70 V 830" stroke="#d4b76e" stroke-width="2" opacity="0.8"/>
<text x="1142" y="88" fill="#f2dda0" font-family="Georgia,serif" font-size="25" letter-spacing="3" text-anchor="middle">BETTING TABLE</text>
<text x="1142" y="113" fill="#c9b98e" font-family="Georgia,serif" font-size="14" letter-spacing="1" text-anchor="middle">EUROPEAN · SINGLE ZERO</text>
{''.join(number_cells)}
<text x="1142" y="337" fill="#f2dda0" font-family="Georgia,serif" font-size="17" letter-spacing="2" text-anchor="middle">BET OPTIONS</text>
{''.join(option_rows)}
<g id="spin-display">
<rect x="930" y="712" width="424" height="118" rx="7" fill="#192820" stroke="#786443" stroke-width="2"/>
<text x="952" y="750" fill="#f2dda0" font-family="Georgia,serif" font-size="17" letter-spacing="2">SPINNING</text>
<text x="952" y="787" fill="#f8f1e1" font-family="Georgia,serif" font-size="20">The marble is circling the wheel...</text>
</g>
<g id="winner-display">
<rect x="930" y="712" width="424" height="118" rx="7" fill="#192820" stroke="#f0d58b" stroke-width="3"/>
<text x="952" y="746" fill="#f2dda0" font-family="Georgia,serif" font-size="15" letter-spacing="2">WINNING POCKET</text>
<circle cx="980" cy="790" r="26" fill="{winning_swatch}" stroke="#f0d58b" stroke-width="2"/>
<text x="980" y="798" fill="#fff8e8" font-family="Georgia,serif" font-size="23" font-weight="700" text-anchor="middle">{winning_number}</text>
<text x="1022" y="787" fill="#fff8e8" font-family="Georgia,serif" font-size="22" font-weight="700">{winning_color.upper()}</text>
<text x="1022" y="811" fill="#c9b98e" font-family="Georgia,serif" font-size="14" letter-spacing="1">{winning_detail}</text>
</g>
</svg>'''

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".svg", prefix="roulette-wheel-", encoding="utf-8", delete=False
    ) as image_file:
        image_file.write(svg)
        image_path = Path(image_file.name)

    if not webbrowser.open_new_tab(image_path.as_uri()):
        print(f"Could not open the wheel automatically: {image_path}")
    return image_path


def roulette_game(money):
    import json
    import threading
    import webbrowser
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    page = '''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>European Roulette</title>
  <style>
    :root { color-scheme: dark; --felt: #12392e; --felt-light: #1b4c3c; --gold: #dfc277; --paper: #f5f0e4; --red: #bd2637; --black: #181a19; }
    * { box-sizing: border-box; }
    body { margin: 0; min-height: 100vh; color: var(--paper); background: radial-gradient(ellipse at 24% 18%, #285947 0, var(--felt) 54%, #0c261f 100%); font-family: Georgia, 'Times New Roman', serif; }
    header { display: flex; align-items: baseline; justify-content: space-between; gap: 24px; max-width: 1320px; margin: auto; padding: 20px 28px 10px; border-bottom: 1px solid #dfc27755; }
    h1 { margin: 0; color: var(--gold); font-size: 28px; font-weight: 500; }
    .balance { font-family: system-ui, sans-serif; font-size: 15px; }
    .balance strong { color: #fff; font-size: 21px; }
    main { display: grid; grid-template-columns: minmax(340px, 1.1fr) minmax(360px, .9fr); gap: 30px; max-width: 1320px; margin: auto; padding: 28px; }
    .wheel-area { display: grid; align-content: start; justify-items: center; }
    #wheel { display: block; width: min(100%, 620px); height: auto; overflow: visible; filter: drop-shadow(0 18px 28px #07171099); }
    #wheel-spin, #ball-spin { transform-box: view-box; transform-origin: 250px 250px; }
    .pointer { fill: #f6e3a7; stroke: #49391f; stroke-width: 3; }
    .wheel-title { fill: #f3d68e; font: 700 16px Georgia, serif; letter-spacing: 2px; text-anchor: middle; }
    .wheel-subtitle { fill: #c6a967; font: 10px Georgia, serif; letter-spacing: 2px; text-anchor: middle; }
    .ball { fill: #fffef5; stroke: #95815a; stroke-width: 3; }
    .table { align-self: start; }
    .table-heading { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }
    h2 { margin: 0; color: var(--gold); font-size: 19px; font-weight: 500; letter-spacing: 1px; }
    .hint { margin: 5px 0 12px; color: #d4c7a2; font: 12px system-ui, sans-serif; }
    .numbers { display: grid; grid-template-columns: repeat(12, minmax(24px, 1fr)); gap: 4px; }
    button { color: var(--paper); font: inherit; cursor: pointer; }
    .number { min-height: 42px; border: 1px solid #dfc277; border-radius: 3px; font: 700 14px Georgia, serif; }
    .number.red, .swatch.red { background: var(--red); }
    .number.black, .swatch.black { background: var(--black); }
    .number.zero { grid-column: 1 / -1; background: #167447; }
    .number.selected, .number.winner { outline: 3px solid #ffe08a; outline-offset: 1px; z-index: 1; }
    .number.selected::after { content: ' BET'; display: block; color: #ffe08a; font: 700 9px system-ui, sans-serif; }
    .number.winner { box-shadow: 0 0 0 5px #fff5d055; }
    .options { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 7px; margin-top: 16px; }
    .bet-option { display: flex; align-items: center; gap: 9px; min-height: 39px; padding: 6px 10px; border: 1px solid #d6bf7b77; border-radius: 3px; background: #142c24; text-align: left; font: 14px system-ui, sans-serif; }
    .bet-option.selected { border: 2px solid var(--gold); background: #244637; }
    .swatch { width: 18px; height: 18px; flex: 0 0 18px; border: 1px solid #ddcc9b; border-radius: 3px; }
    .swatch.neutral { background: #87958b; }
    .wager { display: flex; gap: 10px; margin-top: 18px; }
    .wager label { display: grid; gap: 6px; flex: 1; color: #e0d6bd; font: 12px system-ui, sans-serif; }
    input { width: 100%; min-height: 42px; padding: 8px 10px; border: 1px solid #d6bf7b88; border-radius: 3px; background: #102a21; color: white; font: 16px system-ui, sans-serif; }
    #spin { min-width: 128px; align-self: end; min-height: 42px; border: 1px solid #f0d58b; border-radius: 3px; background: #aa2634; color: white; font: 700 14px system-ui, sans-serif; }
    #spin:disabled { opacity: .45; cursor: not-allowed; }
    #status { min-height: 58px; margin: 15px 0 0; color: #f4e8c5; font: 15px/1.45 system-ui, sans-serif; }
    #return { min-height: 38px; padding: 7px 12px; border: 1px solid #d6bf7b88; border-radius: 3px; background: transparent; color: #e7d6a5; font: 13px system-ui, sans-serif; }
    #return:disabled { opacity: .5; }
    @media (max-width: 760px) { header { padding: 17px 16px 10px; } main { grid-template-columns: 1fr; gap: 10px; padding: 18px 16px 30px; } #wheel { width: min(100%, 440px); } .table { width: 100%; } .number { min-height: 36px; } }
    @media (max-width: 390px) { .numbers { gap: 2px; } .number { min-height: 32px; font-size: 12px; } .options { grid-template-columns: 1fr; } }
  </style>
</head>
<body>
  <header><h1>European Roulette</h1><div class="balance">Balance <strong id="balance">$__BALANCE__</strong></div></header>
  <main>
    <section class="wheel-area" aria-label="Roulette wheel">
      <svg id="wheel" viewBox="0 0 500 500" role="img" aria-label="Single-zero roulette wheel">
        <circle cx="250" cy="250" r="235" fill="#171817" stroke="#b08a4c" stroke-width="10"/>
        <g id="wheel-spin"><circle cx="250" cy="250" r="220" fill="#302619" stroke="#e1c477" stroke-width="4"/><g id="pockets"></g><circle cx="250" cy="250" r="182" fill="none" stroke="#f0d58b" stroke-width="4"/><circle cx="250" cy="250" r="112" fill="#bd9852" stroke="#f0d58b" stroke-width="4"/><circle cx="250" cy="250" r="104" fill="#29221b" stroke="#806137" stroke-width="3"/><circle cx="250" cy="250" r="75" fill="#17241e" stroke="#e0c276" stroke-width="3"/><text x="250" y="244" class="wheel-title">EUROPEAN</text><text x="250" y="270" class="wheel-subtitle">SINGLE ZERO</text></g>
        <g id="ball-spin"><circle class="ball" cx="250" cy="78" r="9"/></g>
        <path class="pointer" d="M250 12 L239 38 L261 38 Z"/>
      </svg>
      <p id="status" role="status" aria-live="polite">Choose a bet and wager, then spin.</p>
      <button id="return" type="button">Return to game center</button>
    </section>
    <section class="table" aria-label="Betting table">
      <div class="table-heading"><h2>Betting table</h2><span class="hint">0–36 · Single zero</span></div>
      <p class="hint">Select an outside bet or choose a number.</p>
      <div class="numbers" id="numbers"></div>
      <div class="options" id="options">
        <button class="bet-option" data-bet="red"><span class="swatch red"></span>Red</button>
        <button class="bet-option" data-bet="black"><span class="swatch black"></span>Black</button>
        <button class="bet-option" data-bet="even"><span class="swatch neutral"></span>Even</button>
        <button class="bet-option" data-bet="odd"><span class="swatch neutral"></span>Odd</button>
        <button class="bet-option" data-bet="low"><span class="swatch neutral"></span>Low · 1–18</button>
        <button class="bet-option" data-bet="high"><span class="swatch neutral"></span>High · 19–36</button>
      </div>
      <div class="wager"><label>Wager amount<input id="amount" type="number" min="1" step="1" value="10"></label><button id="spin" type="button">Spin</button></div>
    </section>
  </main>
<script>
const pocketOrder = [0,32,15,19,4,21,2,25,17,34,6,27,13,36,11,30,8,23,10,5,24,16,33,1,20,14,31,9,22,18,29,7,28,12,35,3,26];
const redNumbers = new Set([1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]);
const svgNS = 'http://www.w3.org/2000/svg';
const pockets = document.getElementById('pockets');
const numbers = document.getElementById('numbers');
const wheel = document.getElementById('wheel-spin');
const ball = document.getElementById('ball-spin');
const amountInput = document.getElementById('amount');
const spinButton = document.getElementById('spin');
const statusText = document.getElementById('status');
const balanceText = document.getElementById('balance');
let balance = Number('__BALANCE__');
let selectedBet = 'red';
let selectedNumber = null;
let spinning = false;

function polar(radius, angle) { return [250 + radius * Math.cos(angle), 250 + radius * Math.sin(angle)]; }
function drawWheel() {
  pocketOrder.forEach((number, index) => {
    const start = -Math.PI / 2 + index * Math.PI * 2 / 37 + .004;
    const end = -Math.PI / 2 + (index + 1) * Math.PI * 2 / 37 - .004;
    const outerStart = polar(169, start), outerEnd = polar(169, end);
    const innerEnd = polar(112, end), innerStart = polar(112, start);
    const path = document.createElementNS(svgNS, 'path');
    path.setAttribute('d', `M${outerStart[0]} ${outerStart[1]} A169 169 0 0 1 ${outerEnd[0]} ${outerEnd[1]} L${innerEnd[0]} ${innerEnd[1]} A112 112 0 0 0 ${innerStart[0]} ${innerStart[1]} Z`);
    path.setAttribute('fill', number === 0 ? '#167447' : redNumbers.has(number) ? '#bd2637' : '#17191a');
    path.setAttribute('stroke', '#dfc277');
    path.setAttribute('stroke-width', '1');
    pockets.append(path);
    const mid = (start + end) / 2;
    const [x,y] = polar(140, mid);
    const label = document.createElementNS(svgNS, 'text');
    label.textContent = number;
    label.setAttribute('x', x); label.setAttribute('y', y);
    label.setAttribute('fill', '#fff8e8'); label.setAttribute('font-size', '10');
    label.setAttribute('font-family', 'Georgia,serif'); label.setAttribute('font-weight', 'bold');
    label.setAttribute('text-anchor', 'middle'); label.setAttribute('dominant-baseline', 'middle');
    label.setAttribute('transform', `rotate(${(mid * 180 / Math.PI) + 90} ${x} ${y})`);
    pockets.append(label);
  });
  const zero = makeNumberButton(0);
  zero.classList.add('zero');
  numbers.append(zero);
  for (let number = 1; number <= 36; number++) numbers.append(makeNumberButton(number));
}
function makeNumberButton(number) {
  const button = document.createElement('button');
  button.type = 'button'; button.className = 'number'; button.textContent = number;
  if (number === 0) button.classList.add('zero');
  else button.classList.add(redNumbers.has(number) ? 'red' : 'black');
  button.dataset.number = number;
  button.addEventListener('click', () => { selectedBet = 'number'; selectedNumber = number; updateSelection(); });
  return button;
}
function updateSelection() {
  document.querySelectorAll('.bet-option').forEach(button => button.classList.toggle('selected', button.dataset.bet === selectedBet));
  document.querySelectorAll('.number').forEach(button => button.classList.toggle('selected', selectedBet === 'number' && Number(button.dataset.number) === selectedNumber));
  spinButton.disabled = spinning || balance < 1 || (selectedBet === 'number' && selectedNumber === null);
}
document.querySelectorAll('.bet-option').forEach(button => button.addEventListener('click', () => { selectedBet = button.dataset.bet; selectedNumber = null; updateSelection(); }));
document.getElementById('options').insertAdjacentHTML('beforeend', '<button class="bet-option" data-bet="number"><span class="swatch neutral"></span>Straight number</button>');
document.querySelector('[data-bet="number"]').addEventListener('click', () => { selectedBet = 'number'; selectedNumber = null; updateSelection(); statusText.textContent = 'Choose a number in the grid.'; });
document.getElementById('return').addEventListener('click', async () => { await fetch('/finish', {method:'POST'}); statusText.textContent = 'Returned to the game center. You can close this tab.'; document.getElementById('return').disabled = true; spinButton.disabled = true; });
spinButton.addEventListener('click', async () => {
  const amount = Number(amountInput.value);
  if (!Number.isInteger(amount) || amount < 1 || amount > balance) { statusText.textContent = 'Enter a whole-number wager within your balance.'; return; }
  if (selectedBet === 'number' && selectedNumber === null) { statusText.textContent = 'Choose a number in the grid.'; return; }
  spinning = true; updateSelection();
  try {
    const response = await fetch('/spin', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({amount, bet:selectedBet, number:selectedNumber})});
    const outcome = await response.json();
    if (!response.ok) throw new Error(outcome.error || 'Could not place that bet.');
    const index = pocketOrder.indexOf(outcome.number);
    const wheelDegrees = 360 * 8 - index * 360 / 37;
    const duration = matchMedia('(prefers-reduced-motion: reduce)').matches ? 1 : 6000;
    const wheelAnimation = wheel.animate([{transform:'rotate(0deg)'},{transform:`rotate(${wheelDegrees}deg)`}], {duration,easing:'cubic-bezier(.12,.78,.18,1)',fill:'forwards'});
    const ballAnimation = ball.animate([{transform:'rotate(0deg)'},{transform:'rotate(-2880deg)'}], {duration,easing:'cubic-bezier(.12,.78,.18,1)',fill:'forwards'});
    statusText.textContent = 'The marble is spinning opposite the wheel...';
    await Promise.all([wheelAnimation.finished, ballAnimation.finished]);
    balance = outcome.balance; balanceText.textContent = '$' + balance.toLocaleString();
    document.querySelectorAll('.number').forEach(button => button.classList.toggle('winner', Number(button.dataset.number) === outcome.number));
    statusText.textContent = `${outcome.number} · ${outcome.color.toUpperCase()} · ${outcome.detail}. ${outcome.won ? 'You won $' + outcome.payout.toLocaleString() + '.' : 'You lost $' + amount.toLocaleString() + '.'}`;
    amountInput.max = balance; amountInput.value = Math.min(Number(amountInput.value), balance) || (balance ? 1 : 0);
  } catch (error) { statusText.textContent = error.message; }
  spinning = false; updateSelection();
});
drawWheel(); updateSelection();
window.addEventListener('pagehide', () => navigator.sendBeacon('/finish', new Blob([], {type:'application/json'})));
</script>
</body>
</html>'''.replace("__BALANCE__", str(money))

    state = {"money": money}
    finished = threading.Event()

    class RouletteHandler(BaseHTTPRequestHandler):
        def log_message(self, format_string, *args):
            pass

        def send_json(self, status, payload):
            body = json.dumps(payload).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.path != "/":
                self.send_error(404)
                return
            body = page.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_POST(self):
            if self.path == "/finish":
                finished.set()
                self.send_json(200, {"balance": state["money"]})
                return
            if self.path != "/spin":
                self.send_error(404)
                return

            try:
                body_length = int(self.headers.get("Content-Length", "0"))
                wager = json.loads(self.rfile.read(body_length))
                amount = wager.get("amount")
                bet_type = wager.get("bet")
                chosen_number = wager.get("number")
                if type(amount) is not int or amount < 1 or amount > state["money"]:
                    raise ValueError("Enter a valid wager within your balance.")
                if bet_type not in {"number", "red", "black", "even", "odd", "low", "high"}:
                    raise ValueError("Choose a valid bet option.")
                if bet_type == "number" and (type(chosen_number) is not int or not 0 <= chosen_number <= 36):
                    raise ValueError("Choose a number from 0 to 36.")

                winning_number = random.randint(0, 36)
                red_numbers = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
                color = "green" if winning_number == 0 else "red" if winning_number in red_numbers else "black"
                won = (
                    (bet_type == "number" and chosen_number == winning_number)
                    or bet_type == color
                    or (bet_type == "even" and winning_number != 0 and winning_number % 2 == 0)
                    or (bet_type == "odd" and winning_number % 2 == 1)
                    or (bet_type == "low" and 1 <= winning_number <= 18)
                    or (bet_type == "high" and 19 <= winning_number <= 36)
                )
                payout = amount * 35 if won and bet_type == "number" else amount if won else 0
                state["money"] += payout if won else -amount
                detail = "Zero" if winning_number == 0 else (
                    f"{'Even' if winning_number % 2 == 0 else 'Odd'}, "
                    f"{'Low' if winning_number <= 18 else 'High'}"
                )
                self.send_json(200, {
                    "number": winning_number,
                    "color": color,
                    "detail": detail,
                    "won": won,
                    "payout": payout,
                    "balance": state["money"],
                })
            except (ValueError, TypeError, json.JSONDecodeError) as error:
                self.send_json(400, {"error": str(error)})

    server = ThreadingHTTPServer(("127.0.0.1", 0), RouletteHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    url = f"http://127.0.0.1:{server.server_port}/"
    if not webbrowser.open_new_tab(url):
        print(f"Open this roulette tab: {url}")
    print("Roulette is running in the browser tab. Return here after closing it or choosing Return to game center.")
    try:
        finished.wait()
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()
        server.server_close()
    return state["money"]


def gambling_game(starting_money=50):
    ##Gambling game function this enables gambling/betting in the other games
    print("\n=== Gambling ===")
    print(f"Starting balance: ${format_balance(starting_money)}")
    money = starting_money
    ##Calls the respective games 
    while True:
        print(f"\nCurrent balance: ${format_balance(money)}")
        print("--- Games ---")
        print("1. Dice Guessing")
        print("2. Poker")
        print("3. Blackjack")
        print("4. Number Guessing")
        print("5. Hangman")
        print("6. Rock Paper Scissors")
        print("7. Roulette")
        print("8. Leave Gambling")
        print("9. Quit")
        print("10. Add money")
        game_choice = input("Choose a gambling game (1-10): ").strip()
        

        if game_choice == "8":
            print("Leaving the gambling table...")
            return
        elif game_choice == "9":
            print("Thanks for playing! Final balance:", f"${format_balance(money)}")
            return "exit"
        elif game_choice == "10":
            new_balance = multiplication_game()
            if new_balance is not None:
                money = new_balance
            continue

        if game_choice == "7":
            money = roulette_game(money)
            if money <= 0:
                print("You are out of money. Game over!")
                return
            continue

        if game_choice not in {"1", "2", "3", "4", "5", "6"}:
            print("Invalid choice. Please choose 1 through 10.")
            continue

        print("\n--- Betting ---")
        bet = get_bet(money)
        if bet is None:
            print("Thanks for playing! Final balance:", f"${format_balance(money)}")
            return

        if game_choice == "1":
            guess = input("Choose a number from 1 to 6: ").strip()
            try:
                guess = int(guess)
            except ValueError:
                print("Please enter a valid number from 1 to 6.")
                continue

            if guess < 1 or guess > 6:
                print("Your guess must be between 1 and 6.")
                continue

            roll = random.randint(1, 6)
            print("Rolling the dice...")
            time.sleep(0.5)
            print("The dice rolled a", roll)

            if guess == roll:
                money += bet
                print("You win! You earned your bet.")
            else:
                money -= bet
                print("You lose this round.")

        elif game_choice == "2":
            money = poker_game(money, bet)
        elif game_choice == "3":
            money = blackjack_game(money, bet)
        elif game_choice == "4":
            money = number_guessing_game(money, bet)
        elif game_choice == "5":
            money = hangman_game(money, bet)
        elif game_choice == "6":
            money = rock_paper_scissors_game(money, bet)

        if money <= 0:
            print("You are out of money. Game over!")
            return


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


def poker_game(money=0, bet=0):
    print("\n=== Poker ===")
    print("You are dealt 5 cards, and the dealer gets 5 cards. The best hand wins.")
    print("Dealing cards...")
    time.sleep(0.5)
    deck = create_deck()
    player_hand = [deck.pop() for _ in range(5)]
    dealer_hand = [deck.pop() for _ in range(5)]

    print("\nYour hand:")
    for card in player_hand:
        print("-", poker_card_name(card))
    print("\nDealer hand:")
    for card in dealer_hand:
        print("-", poker_card_name(card))

    player_rank, player_tiebreak = poker_score_hand(player_hand)
    dealer_rank, dealer_tiebreak = poker_score_hand(dealer_hand)

    print("Your hand ranking:", poker_hand_rank_name(player_rank), "-", player_tiebreak)
    print("Dealer hand ranking:", poker_hand_rank_name(dealer_rank), "-", dealer_tiebreak)

    if player_rank > dealer_rank or (player_rank == dealer_rank and player_tiebreak > dealer_tiebreak):
        print("You win this poker round!")
        return money + bet
    elif player_rank < dealer_rank or (player_rank == dealer_rank and player_tiebreak < dealer_tiebreak):
        print("Dealer wins this poker round.")
        return money - bet
    else:
        print("It's a tie in poker.")
        return money


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


def blackjack_game(money=0, bet=0):
    print("\n=== Blackjack ===")
    deck = create_deck()
    player_hand = [deal_card(deck), deal_card(deck)]
    dealer_hand = [deal_card(deck), deal_card(deck)]
    print("Dealing cards...")
    time.sleep(0.5)

    while True:
        show_hand("Player", player_hand)
        print("Dealer shows:", blackjack_card_name(dealer_hand[0]))

        if hand_total(player_hand) == 21:
            print("You hit 21! You win!")
            return money + bet

        if hand_total(player_hand) > 21:
            print("You busted! Dealer wins.")
            return money - bet

        choice = input("Do you want to hit or stand? (h/s): ").strip().lower()

        if choice == "h":
            print("Dealing a card...")
            time.sleep(0.5)
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
        print("Dealing a card...")
        time.sleep(0.5)
        show_hand("Dealer", dealer_hand)

    player_total = hand_total(player_hand)
    dealer_total = hand_total(dealer_hand)

    print("\nFinal results:")
    show_hand("Player", player_hand)
    show_hand("Dealer", dealer_hand)

    if dealer_total > 21:
        print("Dealer busted! You win!")
        return money + bet
    elif player_total > dealer_total:
        print("You win!")
        return money + bet
    elif player_total < dealer_total:
        print("Dealer wins!")
        return money - bet
    else:
        print("It's a tie!")
        return money




def show_menu():
    print("\n=== Game Center ===")
    print("1. Number Guessing")
    print("2. Hangman")
    print("3. Rock Paper Scissors")
    print("4. Dice Guessing")
    print("5. Gambling")
    print("6. Exit")
    print("7. Add money to gambling balance")
    print("8. Field Finder")


def launch_browser_game_center():
    import json
    import subprocess
    import threading
    import webbrowser
    from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
    from pathlib import Path
    from urllib.parse import quote, urlsplit

    workspace = Path(__file__).resolve().parents[1]
    subprocess.run([sys.executable, str(workspace / "tmp.py")], check=True)
    finder_index = (workspace / "fields" / "finder_position.txt").read_text(encoding="utf-8").strip()
    game_page = Path(__file__).resolve().with_name("game_center.html")
    finished = threading.Event()

    class GameCenterHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(workspace), **kwargs)

        def log_message(self, format_string, *args):
            pass

        def send_json(self, status, payload):
            response = json.dumps(payload).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)

        def do_POST(self):
            route = urlsplit(self.path).path
            if route == "/finish":
                finished.set()
                self.send_json(200, {"ok": True})
                return
            if route != "/save":
                self.send_error(404)
                return

            try:
                content_length = int(self.headers.get("Content-Length", "0"))
                if not 0 < content_length <= 4096:
                    raise ValueError("Invalid save request.")
                payload = json.loads(self.rfile.read(content_length))
                saved_balance = payload.get("balance")
                if type(saved_balance) is not int or saved_balance < 0:
                    raise ValueError("Balance must be a nonnegative whole number.")
            except (ValueError, TypeError, json.JSONDecodeError) as error:
                self.send_json(400, {"error": str(error)})
                return

            print(f"\nSaved balance from browser: ${saved_balance:,}", flush=True)
            self.send_json(200, {"balance": saved_balance})

    server = ThreadingHTTPServer(("127.0.0.1", 0), GameCenterHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    page_path = quote(game_page.relative_to(workspace).as_posix(), safe="/")
    game_url = f"http://127.0.0.1:{server.server_port}/{page_path}?finder={finder_index}"
    if not webbrowser.open_new_tab(game_url):
        print(f"Open the game center in your browser: {game_url}", flush=True)
    print("Click Save to print the balance here. Choose Exit or close the tab to finish.", flush=True)
    try:
        finished.wait()
    except KeyboardInterrupt:
        print("\nClosing the game center.")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    launch_browser_game_center()