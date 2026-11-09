# Provides the shuffle operation used to randomize the deck.
import random

# The four suits included in a standard deck of playing cards.
SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
# Card values 2-10 are numeric; 11-14 represent Jack, Queen, King, and Ace.
VALUES = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
# Maps the special numeric values to the names shown to the player.
FACE_CARDS = {11: "Jack", 12: "Queen", 13: "King", 14: "Ace", 15: "Joker"}


def create_deck():
    """Build and shuffle a full deck represented as card dictionaries."""
    # Add one card for every combination of suit and value.
    deck = []
    for suit in SUITS:
        for value in VALUES:
            deck.append({"suit": suit, "value": value})

    # Randomize the order so dealing produces a different game each time.
    random.shuffle(deck)
    return deck


def card_name(card):
    """Return a readable name such as 'Queen of Hearts' for a card."""
    value = card["value"]
    # Use a face-card name when available; otherwise show the number.
    if value in FACE_CARDS:
        name = FACE_CARDS[value]
    else:
        name = str(value)
    return f"{name} of {card['suit']}"


def hand_total(hand):
    """Calculate a hand's Blackjack value, counting aces as 1 or 11."""
    total = 0
    # Keep track of aces counted as 11 so they can be reduced to 1 if needed.
    aces = 0

    for card in hand:
        value = card["value"]
        if value == 14:
            aces += 1
            total += 11
        else:
            # Number cards keep their value; face cards count as 10.
            total += min(value, 10)

    # Change aces from 11 to 1 (subtracting 10) until the hand is safe
    # or there are no more aces that can be adjusted.
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total

def deal_card(deck):
    """Draw and remove the next card from the end of the shuffled deck."""
    return deck.pop()


def show_card(card, prefix="  - "):
    """Print a card, using ASCII art for a Joker."""
    if card["value"] != 15:
        print(prefix + card_name(card))
        return

    joker_art = (
        "  .-----------.",
        "  |   JOKER   |",
        "  |    .-.    |",
        "  |   (o o)   |",
        "  |    \\_/    |",
        "  '-----------'",
    )
    for index, line in enumerate(joker_art):
        indentation = prefix if index == 0 else " " * len(prefix)
        print(indentation + line)


def show_hand(name, hand):
    """Print a player's or dealer's cards and the calculated total."""
    print(f"{name}'s hand:")
    for card in hand:
        show_card(card)
    print("Total:", hand_total(hand))


def blackjack_game():
    """Run one complete round of Blackjack between the player and dealer."""
    # Start with a fresh shuffled deck and deal two cards to each side.
    deck = create_deck()
    player_hand = [deal_card(deck), deal_card(deck)]
    dealer_hand = [deal_card(deck), deal_card(deck)]

    # Explain the objective before asking the player to make a move.
    print("\nWelcome to Blackjack!")
    print("Goal: get as close to 21 as possible without going over.")

    # Let the player keep drawing cards ("hit") or end their turn ("stand").
    while True:
        show_hand("Player", player_hand)
        # Only reveal the dealer's first card during the player's turn.
        print("Dealer shows:")
        show_card(dealer_hand[0])

        # End immediately if the player has reached 21 or gone over it.
        if hand_total(player_hand) == 21:
            print("You hit 21! You win!")
            return

        if hand_total(player_hand) > 21:
            print("You busted! Dealer wins.")
            return

        # Normalize the response so inputs like " H " are accepted as "h".
        choice = input("Do you want to hit or stand? (h/s): ").strip().lower()

        if choice == "h":
            # Add one card to the player's hand and show it on the next loop.
            player_hand.append(deal_card(deck))
        elif choice == "s":
            # Leave the player loop and let the dealer take a turn.
            break
        else:
            # Invalid choices do not change either hand; ask again.
            print("Please enter 'h' for hit or 's' for stand.")

    # Reveal the dealer's full hand after the player stands.
    print("\nDealer's turn:")
    show_hand("Dealer", dealer_hand)

    # The dealer follows the standard rule of drawing while below 17.
    while hand_total(dealer_hand) < 17:
        dealer_hand.append(deal_card(deck))
        print("Dealer hits:")
        show_hand("Dealer", dealer_hand)

    # Cache both totals so the final comparison uses the completed hands.
    player_total = hand_total(player_hand)
    dealer_total = hand_total(dealer_hand)

    # Display both final hands before announcing the outcome.
    print("\nFinal results:")
    show_hand("Player", player_hand)
    show_hand("Dealer", dealer_hand)

    # Compare totals, accounting first for the dealer busting.
    if dealer_total > 21:
        print("Dealer busted! You win!")
    elif player_total > dealer_total:
        print("You win!")
    elif player_total < dealer_total:
        print("Dealer wins!")
    else:
        print("It's a tie!")


def main():
    """Run rounds until the player chooses to stop."""
    while True:
        blackjack_game()
        choice = input("Play again? (y/n): ").strip().lower()
        if choice not in ("y", "yes"):
            break


# Start the game when this script is run.
main()
