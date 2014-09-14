"""
``cards`` module provides base classes and APIs for a standard playing card deck.

Should be python 2.7 and python 3.4 compatible.
"""
import random

#from random import shuffle


class NoneList(list):
    """
    """
    def __getitem__(self, index):
        if index is None:
            return None
        else:
            return list.__getitem__(self, index)


class Suits(NoneList):
    def __init__(self, suits=['S','C','H','D']):
        list.__init__(self, suits)


class Ranks(NoneList):
    def __init__(self, ranks=['A', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                              'J', 'Q', 'K']):
        list.__init__(self, ranks)



class Card(object):
    """ A Lonely Card.
          Usage:
            Card('2C')
            Card([suit=index],[rank=index])
    """

    def __init__(self, suit=None, rank=None, up=False, private=True,
                 suits=Suits(), ranks=Ranks()):
        """
        """
        self.suits = suits
        self.ranks = ranks
        self.suit = suit
        self.rank = rank
        self.up = up        # Card is face up and can be seen by all observers.
        self.private = private # Possibly deprecating this usage.

    @classmethod
    def from_str(cls, string, suits=Suits(), ranks=Ranks(), **kwa):
        """Use a "card string" to instantiate the card.
        e.g., "AC" for Ace of Clubs, "A" for suitless Ace.
        """

        if len(string) == 1:
            return cls(rank=ranks.index(string.upper()), **kwa)

        elif len(string) == 2:
            rankstr, suitstr = string.upper()

        elif len(string) == 3: # Case for "10*"
            string = string.upper()
            rankstr, suitstr = string[:2], string[2]

        else:
            raise ValueError("Card ``string`` argument must be a length of 1 "
                             "or 2.")

        return cls(suit=suits.index(suitstr),
                    rank=ranks.index(rankstr), suits=suits, ranks=ranks,
                    **kwa)

    def __eq__(self, other):
        return ((self.suit is None or other.suit is None or
                    self.suit == other.suit) and
                (self.rank is None or other.rank is None or
                    self.rank == other.rank))

    def __iter__(self):
        # This has been reversed to be more logical with the rest of teh class.
        yield self.rank
        yield self.suit

    def serialize(self, snoop=False):
        if any([snoop, self.up]) is True:
            rank = self.ranks[self.rank] or '*'
            suit = self.suits[self.suit] or '*'
        else:
            rank = 'X'
            suit = 'X'
        return "%s%s" % (rank,suit)

    def __json__(self):
        return self.serialize()

    def __repr__(self):
        return ("Card(rank=%s, suit=%s, serialize=%s)" %
                    (self.rank, self.suit, self.serialize(snoop=True)))


class Deck(list):
    """ A Deck of Cards.
        Usage:
            Deck() - Build a Deck of 52 cards of type Card()
    """

    def __init__(self, suits=Suits(), ranks=Ranks(), card_cls=Card,
                 build=True, shuffle=False):
        self.card_cls = card_cls
        self.suits = suits
        self.ranks = ranks
        self.__initlen = 0

        if build is True:
            self.build()

        if shuffle is True:
            self.shuffle()

    def build(self):
        """Build the deck from suits and ranks.
        """
        for suit in range(len(self.suits)):
            for rank in range(len(self.ranks)):
                self.append(self.card_cls(suit=suit, rank=rank,
                                          suits=self.suits, ranks=self.ranks))
        self.__initlen += len(self)

    def wipe(self):
        list.__init__(self)
        self.__initlen = 0

    def reset(self):
        self.wipe()
        self.build()

    def shuffle(self, func=None):
        random.shuffle(self, func)

    def check(self, threshold=1):
        return len(self) < threshold * self.__initlen

    def serialize(self, snoop=False):
        """ provides serialization to the class. for json encoding. """
        return [card.serialize(snoop=snoop) for card in self]

    def __json__(self):
        return self.serialize()

    def __repr__(self):
        string = ''
        for card in self:
          string = '%s%s,' % (string, card.serialize(snoop=True))

        return "Deck(%s)" % string[:-1]


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


# (c) 2011-2014 StudioCoda & Nicholas Long. All Rights Reserved