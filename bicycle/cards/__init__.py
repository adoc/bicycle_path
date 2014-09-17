"""
``cards`` module provides base classes and APIs for a standard playing card deck.

Should be python 2.7 and python 3.4 compatible.
"""

import inspect
import itertools
import functools
import random

#  overload random with os.urandom
random = random.SystemRandom()


#suits = ['S','D','C','H']
#ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']




class DeckTypeStandard(object):
    """Contains the fundamental state of a standard playing deck.
    (i.e., Suits and Ranks.)

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

    def ranks_index(self, rank):
        return self.__ranks.index(rank)

    def suits_index(self, suit):
        return self.__suits.index(suit)

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
        e.g., "AC" for Ace of Clubs, "A" for suitless Ace.
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
        # Is this even used???
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


class Hand(list):
    """ A list of ``Card``s """

    def __init__(self, deck_type=DeckTypeStandard, card_cls=Card,
                 build=True, shuffle=False):
        self.card_cls = card_cls
        self.deck_type = inspect.isclass(deck_type) and deck_type() or deck_type
        self._initlen = 0

    def serialize(self, snoop=False):
        """ provides serialization to the class. for json encoding. """
        return [card.serialize(snoop=snoop) for card in self]

    def __json__(self):
        return self.serialize()

    def __repr__(self):
        return "Hand(%s)" % ','.join(self.serialize(snoop=True))


class Deck(Hand): 
    """ A Deck of Cards.
        Usage:
            Deck() - Build a Deck of 52 cards of type Card()
    """

    def __init__(self, build=True, shuffle=False, **kwa):
        Hand.__init__(self, **kwa)

        if build is True:
            self.build()

        if shuffle is True:
            self.shuffle()

    def build(self):
        """Build the deck from suits and ranks.
        """
        for suit, rank in self.deck_type.build():
            self.append(self.card_cls(suit, rank, deck_type=self.deck_type))
        self._initlen += len(self)

    def wipe(self):
        list.__init__(self)
        self._initlen = 0

    def reset(self):
        self.wipe()
        self.build()

    def shuffle(self, func=None):
        random.shuffle(self, func)

    def check(self, threshold=1):
        return len(self) < threshold * self.__initlen

    def __repr__(self):
        return "Deck(%s)" % ','.join(self.serialize(snoop=True))


class Shoe(Deck):
    """ A Shoe of Decks. 
        Usage:
            Shoe(numdecks=1, **deck_kwa)""" 

    def __init__(self, numdecks=1, **kwa):
        self.__numdecks = numdecks
        Deck.__init__(self, **kwa)

    def build(self):
        for _ in range(self.__numdecks):
            Deck.build(self)

    def __repr__(self):
        return "Shoe(%s)" % ','.join(self.serialize(snoop=True))


class DeckEmpty(Exception):
    """
    """

    pass


def deal(deck, hand, iterations=1):
    try:
        for _ in range(iterations):
            hand.append(deck.pop())
    except IndexError: # deck.pop should be the only thing that raises
                       # IndexError, but be wary.
        raise DeckEmpty("Cannot deal from an empty deck.")


# (c) 2011-2014 StudioCoda & Nicholas Long. All Rights Reserved