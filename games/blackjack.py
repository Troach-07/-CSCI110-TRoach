import random


SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
VALUES = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
FACE_CARDS = {11: "Jack", 12: "Queen", 13: "King", 14: "Ace"}


def create_deck():
    deck = []
    for suit in SUITS:
        for value in VALUES:
            deck.append({"suit": suit, "value": value})
    random.shuffle(deck)
    return deck


def card_name(card):
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
        print("  -", card_name(card))
    print("Total:", hand_total(hand))


def blackjack_game():
    deck = create_deck()
    player_hand = [deal_card(deck), deal_card(deck)]
    dealer_hand = [deal_card(deck), deal_card(deck)]

    print("\nWelcome to Blackjack!")
    print("Goal: get as close to 21 as possible without going over.")

    while True:
        show_hand("Player", player_hand)
        print("Dealer shows:", card_name(dealer_hand[0]))

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


blackjack_game()
