import random

VALUES = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
RANK_NAMES = {
    11: "Jack",
    12: "Queen",
    13: "King",
    14: "Ace",
}


def create_deck():
    deck = []
    for suit in SUITS:
        for value in VALUES:
            deck.append({"suit": suit, "value": value})
    random.shuffle(deck)
    return deck


def card_name(card):
    value = card["value"]
    if value in RANK_NAMES:
        value_name = RANK_NAMES[value]
    else:
        value_name = str(value)
    return f"{value_name} of {card['suit']}"


def score_hand(hand):
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


def hand_rank_name(rank_number):
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


print("Welcome to Simple Poker!")
print("You are dealt 5 cards. The best hand wins.")

while True:
    deck = create_deck()
    hand = [deck.pop() for _ in range(5)]
    print("\nYour hand:")
    for card in hand:
        print("-", card_name(card))

    rank, tiebreak = score_hand(hand)
    print("Hand ranking:", hand_rank_name(rank))
    print("Tiebreak value:", tiebreak)

    again = input("Play again? (y/n): ").strip().lower()
    if again != "y":
        print("Thanks for playing!")
        break

