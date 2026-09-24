import random

words = [
    "python",
    "computer",
    "hangman",
    "student",
    "programming",
    "keyboard",
    "library",
    "science",
    "challenge",
    "coffee",
    "teacher",
    "window",
    "planet",
    "rocket",
    "diamond",
    "garden",
    "forest",
    "ocean",
    "mountain",
    "pencil",
    "notebook",
    "holiday",
    "sunshine",
    "rainbow",
    "basketball",
    "football",
    "soccer",
    "baseball",
    "bicycle",
    "universe",
    "language",
    "history",
    "mathematics",
    "friendship",
    "adventure",
    "campfire",
    "backpack",
    "treasure",
    "journey",
    "picture",
    "morning",
    "evening",
    "nightfall",
    "sunset",
    "machine",
    "network",
    "display",
    "monitor",
    "printer",
    "speaker",
    "browser",
    "internet",
    "software",
    "hardware",
    "database",
    "analysis",
    "memory",
    "learning",
    "creativity",
    "festival",
    "campus",
    "camera",
    "message",
    "sunflower",
    "whistle",
    "airplane",
    "castle",
    "marble",
    "lantern",
    "treetop",
    "treasure",
    "sailboat",
    "volcano",
    "butterfly",
    "parade",
    "dragon",
    "puzzle",
    "village",
    "station",
    "gateway",
    "shadow",
    "glacier",
    "thunder",
    "weather",
    "summer",
    "winter",
    "autumn",
    "spring",
    "skeleton",
    "galaxy",
    "jungle",
    "desert",
    "island",
    "harbor",
    "bridge",
    "musical",
    "rhythm",
    "drummer",
    "violin",
    "piano",
    "guitar",
    "concert",
    "trophy",
    "victory",
    "champion",
    "campbell",
    "apples",
    "banana",
    "orange",
    "grape",
    "peach",
    "pear",
    "plum",
    "lemon",
    "mango",
    "strawberry",
    "blueberry",
    "raspberry",
    "pineapple",
    "watermelon",
    "cucumber",
    "tomato",
    "potato",
    "carrot",
    "onion",
    "garlic",
    "pepper",
    "celery",
    "broccoli",
    "spinach",
    "lettuce",
    "avocado",
    "sandwich",
    "salad",
    "pizza",
    "burger",
    "pasta",
    "cookie",
    "donut",
    "waffle",
    "cupcake",
    "chocolate",
    "vanilla",
]

word = random.choice(words)
letters_guessed = []
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

print("Welcome to Hangman!")
print("Guess the word one letter at a time.")

while wrong_guesses < max_wrong:
    display = ""
    for letter in word:
        if letter in letters_guessed:
            display += letter + " "
        else:
            display += "_ "
    print("\n" + hangman[wrong_guesses])
    print("Word:", display)
    print("Guessed letters:", " ".join(letters_guessed) if letters_guessed else "None")
    print(f"Wrong guesses left: {max_wrong - wrong_guesses}")

    guess = input("Enter a letter or type 'quit' to exit: ").strip().lower()

    if guess == "quit":
        print("Thanks for playing! The word was:", word)
        break

    if len(guess) != 1 or not guess.isalpha():
        print("Please enter one letter only.")
        continue

    if guess in letters_guessed:
        print("You already guessed that letter.")
        continue

    letters_guessed.append(guess)

    if guess in word:
        print("Correct!")
    else:
        wrong_guesses += 1
        print("Incorrect! That letter is not in the word.")

    if all(letter in letters_guessed for letter in set(word)):
        print("\nYou win! The word was:", word)
        break

else:
    print("\n" + hangman[max_wrong])
    print("\nYou ran out of guesses! The word was:", word)

print("\nThanks for playing!")
