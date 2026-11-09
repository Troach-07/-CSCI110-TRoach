# Outside resources: the assignment's A New Alphabet problem statement.
# No other outside resources were used.

import sys

# Algorithm:
# 1. Read the input line.
# 2. Translate each letter using the mapping, ignoring letter case.
# 3. Keep every character that is not an English letter unchanged.
# 4. Print the translated line.

TRANSLATIONS = {
    "a": "@",
    "b": "8",
    "c": "(",
    "d": "|)",
    "e": "3",
    "f": "#",
    "g": "6",
    "h": "[-]",
    "i": "|",
    "j": "_|",
    "k": "|<",
    "l": "1",
    "m": "[]\\/[]",
    "n": "[]\\[]",
    "o": "0",
    "p": "|D",
    "q": "(,)",
    "r": "|Z",
    "s": "$",
    "t": "']['",
    "u": "|_|",
    "v": "\\/",
    "w": "\\/\\/",
    "x": "}{",
    "y": "`/",
    "z": "2",
}


def translate_character(character):
    """Return the New Alphabet equivalent, or the original character."""
    return TRANSLATIONS.get(character.lower(), character)


def translate_text(text):
    """Translate each character in a string and return the resulting text."""
    return "".join(translate_character(character) for character in text)


def main():
    """Read one line from standard input and print its translation."""
    text = sys.stdin.readline().rstrip("\n")
    print(translate_text(text))


if __name__ == "__main__":
    main()