"""
``cards`` module provides base classes and APIs for a standard playing
card deck.

Should be python 2.7 and python 3.4 compatible.
"""

import inspect
import functools

from bicycle import random      # Always import ``random`` from the
                                #   ``bicycle`` module as it provides
                                #   extra entropy.


class DeckTypeStandard(object):
    """Contains the fundamental state of a standard playing deck.
    (i.e., Suits and Ranks.)

    Cards in a standard deck are abbreviated and always referenced by
    Rank then Suit. "AS" is the Ace of Spades. "KQ" is the King of
    Queens, and so on.

    The Ace is low (index 0) in this configuration. Games where the Ace
    is high should attempt to overload the ``Card`` or ``Cards`` class
    as demonstrated in ``blackjack.Hand`` to account for an Ace being
    high.

    ``build`` method iterates suits then ranks and yields suit_str
            then rank_str.
    """
    def __init__(self, suits=['S','D','C','H'], 
                 ranks=['A', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                             'J', 'Q', 'K']):
        self.__suits = suits
        self.__ranks = ranks

    def build(self):
        for suit_str in self.__suits:
            for rank_str in self.__ranks:
                yield self.suits_index(suit_str), self.ranks_index(rank_str)

    def ranks_index(self, rank_str):
        return self.__ranks.index(rank_str)

    def suits_index(self, suit_str):
        return self.__suits.index(suit_str)

    def get_rank(self, rank_index):
        return self.__ranks[rank_index]

    def get_suit(self, suit_index):
        return self.__suits[suit_index]


@functools.total_ordering
class Card(object):
    """ A Lonely Card.
          Usage:
            Card('2C')
            Card([suit=index],[rank=index])
    """

    def __init__(self, suit, rank, up=False,
                 private=True, deck_type=DeckTypeStandard):
        """
        """
        self.deck_type = inspect.isclass(deck_type) and deck_type() or deck_type
        self.suit = suit
        self.rank = rank
        self.up = up        # Card is face up and can be seen by all observers.
        self.private = private # Possibly deprecating this usage.

    @classmethod
    def from_str(cls, string, deck_type=DeckTypeStandard, **kwa):
        """Use a "card string" to instantiate the card.
        e.g., "AC" for Ace of Clubs.
        """

        deck_type = inspect.isclass(deck_type) and deck_type() or deck_type

        # if len(string) == 1:
        #     return cls(rank=deck_type.ranks_index(string.upper()), **kwa)

        if len(string) == 2:
            rankstr, suitstr = string.upper()

        elif len(string) == 3: # Case for "10*"
            string = string.upper()
            rankstr, suitstr = string[:2], string[2]

        else:
            raise ValueError("Card ``string`` argument must be a length of 2 "
                             "or 3.")

        return cls(deck_type.suits_index(suitstr),
                    deck_type.ranks_index(rankstr), deck_type=deck_type,
                    **kwa)

    def __lt__(self, other):
        return self.rank < other.rank

    def __eq__(self, other):
        return self.rank == other.rank

    def __iter__(self):
        # This has been reversed to be more logical with the rest of teh class.
        # Is this even used??? or needed?
        yield self.rank
        yield self.suit

    def serialize(self, snoop=False):
        """

        When ``snoop`` is True, ignore the ``up`` and ``private``
        instance attributes.
        """

        if any([snoop, self.up]) is True:
            rank = self.deck_type.get_rank(self.rank) or '*'
            suit = self.deck_type.get_suit(self.suit) or '*'
        else:
            rank = 'X'
            suit = 'X'
        return "%s%s" % (rank,suit)

    def __json__(self):
        return self.serialize()

    def __repr__(self):
        return ("Card(rank=%s, suit=%s, serialize=%s)" %
                    (self.rank, self.suit, self.serialize(snoop=True)))


class Cards(list):
    """ A list of ``Card``s
    """

    def __init__(self):
        list.__init__(self)
        self.initlen = 0

    def serialize(self, snoop=False):
        """ provides serialization to the class. for json encoding. """
        return [card.serialize(snoop=snoop) for card in self]

    def __json__(self):
        return self.serialize()

    def __repr__(self):
        return "Cards(%s)" % ','.join(self.serialize(snoop=True))


class DeckEmpty(Exception):
    """
    """

    pass


class DeckLow(Exception):
    """
    """

    pass


shuffle = random.shuffle


def build(deck, numdecks=1, card_cls=Card, deck_type=DeckTypeStandard, do_shuffle=False):
    """Build a  ``deck`` or Shoe.
    """
    deck_type = inspect.isclass(deck_type) and deck_type() or deck_type
    for _ in range(numdecks):
        for suit, rank in deck_type.build():
            deck.append(card_cls(suit, rank, deck_type=deck_type))

    deck.initlen += len(deck)
    if do_shuffle is True:
        return shuffle(deck)
    else:
        return deck


def wipe(cards):
    cards.wipe()


def check(cards, threshold=1):
    """Check the cards based on a ``threshold`` factor of its original
    length.
    """

    return len(cards) < threshold * cards.initlen


# These deal funcs are simple and obvious now, but might include card
#   state changes which makes more sense.

def deal(deck, hand, iterations=1, do_check=False):
    """Deal a card from the ``deck`` to the ``hand``.
    """

    try:
        for _ in range(iterations):
            hand.append(deck.pop())
    except IndexError: # deck.pop should be the only thing that raises
                       # IndexError, but be wary.
        raise DeckEmpty("Cannot deal from an empty deck.")

def deal_all(source, target):
    try:
        while True:
            target.append(source.pop())
    except IndexError:
        pass



# (c) 2011-2014 StudioCoda & Nicholas Long. All Rights Reserved