from __future__ import annotations
import numpy as np
FILENAME = '7.txt'

RANK_MAP = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14
}

REVERSED_RANK_MAP = {v: k for k, v in RANK_MAP.items()}
REVERSED_RANK_MAP[1] = 'J'


class Card:
    def __init__(self, card):
        self.rank = RANK_MAP[card]
        # For printing purposes

    def __eq__(self, other: Card):
        return self.rank == other.rank

    def __lt__(self, other: Card):
        return self.rank < other.rank

    def __gt__(self, other: Card):
        return self.rank > other.rank

    def __hash__(self):
        return hash(self.rank)

    def __str__(self):
        return REVERSED_RANK_MAP[self.rank]

    def __repr__(self):
        return str(self)


joker_card = Card('J')
joker_card.rank = 1


class Hand:
    def __init__(self, cards, with_jokers=False):
        self.cards = cards
        self.joker_cards = self.cards.count(joker_card)
        self.strength = self.count_strength(with_jokers)

    def __eq__(self, other: Hand):
        return self.strength == other.strength

    def __lt__(self, other: Hand):
        if not self.strength == other.strength:
            return self.strength < other.strength
        else:
            # Compare cards depending on rank one by one
            for c1, c2 in zip(self.cards, other.cards):
                if c1 < c2:
                    return True
                elif c1 > c2:
                    return False
            return False

    def count_strength(self, with_jokers=False):
        combos = [self.five_of_a_kind, self.four_of_a_kind, self.full_house,
                  self.three_of_a_kind, self.two_pairs, self.one_pair, self.high_card]
        strength = 7
        for combo in combos:
            if combo(with_jokers):
                break
            else:
                strength -= 1
        return strength

    def five_of_a_kind(self, with_jokers=False):
        # Detects whether all cards are the same
        if len(set(self.cards)) == 1:
            return True
        elif with_jokers:
            if self.joker_cards == 4:
                return True
            elif self.joker_cards >= 2:
                return self.full_house()
            elif self.joker_cards == 1:
                return self.four_of_a_kind()
            else:
                return False
        else:
            return False

    def four_of_a_kind(self, with_jokers=False):
        # Detects whether there are 4 cards of the same value
        if len(set(self.cards)) == 2:
            for card in set(self.cards):
                if self.cards.count(card) == 4:
                    return True
        elif with_jokers:
            if self.joker_cards == 3:
                return True
            elif self.joker_cards == 2:
                return self.two_pairs()
            elif self.joker_cards == 1:
                return self.three_of_a_kind()
            else:
                return False
        else:
            return False

    def full_house(self, with_jokers=False):
        card_counts = []
        if len(set(self.cards)) == 2:
            for card in set(self.cards):
                card_counts.append(self.cards.count(card))
            if 3 in card_counts:
                return True
        elif with_jokers:
            if self.joker_cards == 1:
                return self.two_pairs() or self.three_of_a_kind()
            elif self.joker_cards == 2:
                return self.two_pairs() or self.three_of_a_kind()
        return False

    def three_of_a_kind(self, with_jokers=False):
        for card in set(self.cards):
            if self.cards.count(card) == 3:
                return True
        if with_jokers:
            if self.joker_cards == 1:
                return self.one_pair()
            elif self.joker_cards == 2:
                return True
        else:
            return False

    def two_pairs(self, with_jokers=False):
        pair_count = 0
        for card in set(self.cards):
            if self.cards.count(card) == 2:
                pair_count += 1
        if pair_count == 2:
            return True
        if with_jokers:
            if self.joker_cards == 1:
                return self.one_pair()
            elif self.joker_cards == 2:
                return True
        return False

    def one_pair(self, with_jokers=False):
        for card in set(self.cards):
            if self.cards.count(card) == 2:
                return True
        if with_jokers:
            if self.joker_cards == 1:
                return True
        else:
            return False

    def high_card(self, with_jokers=False):
        return True

    def __str__(self):
        return str(self.cards)

    def __repr__(self):
        return str(self.cards)


def read_cards(cards, with_jokers=False):
    if with_jokers:
        return [joker_card if card == 'J' else Card(card) for card in cards]
    else:
        return [Card(card) for card in cards]


def read_input(filename, with_jokers=False):
    hands, bids = [], []
    with open(filename) as f:
        for line in f:
            hand_s, bid = line.split(' ')
            bids.append(int(bid))
            hands.append(
                Hand(read_cards(hand_s, with_jokers=with_jokers), with_jokers=with_jokers))
    return hands, bids


hands, bids = read_input(FILENAME)
# First part
sorted_bids = sorted(bids, key=lambda bid: hands[bids.index(bid)])
sorted_bids = np.array(sorted_bids)
rank = np.arange(1, len(bids)+1)
print(sum(rank*sorted_bids))

# Second part


hands, bids = read_input(
    FILENAME, with_jokers=True)

sorted_bids = sorted(bids, key=lambda bid: hands[bids.index(bid)])
sorted_bids = np.array(sorted_bids)
rank = np.arange(1, len(bids)+1)
print(sum(rank*sorted_bids))
