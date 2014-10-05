"""
``cards`` module provides base classes and APIs for a standard playing
card deck.

Should be python 2.7 and python 3.4 compatible.
"""

import inspect
import functools

import bicycle.marshal

from bicycle import random      # Always import ``random`` from the
                                #   ``bicycle`` module as it provides
                                #   extra entropy.

shuffle = random.shuffle


try:
    range = xrange
except NameError:
    pass


# Exceptions
# ==========
class DeckEmpty(Exception):
    """
    """

    pass


class DeckLow(Exception):
    """
    """

    pass


# Base Class
# ==========

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


# Card Class
# ==========
@functools.total_ordering
class Card(object):
    """ A Lonely Card.
          Usage:
            Card(suit_index, rank_index)
            Card.from_str('2C')
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
    def build(cls, deal_idx=0, **kwa):
        """Build a deck based on this class of `Card`.
        """
        return Cards(deal_idx).build(card_cls=cls, **kwa)

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

    def __int__(self):
        """Return "Face" value. (11, 12, 13 for J, Q, K.)
        """

        return self.rank + 1

    def __eq__(self, other):
        """Equivalence. Base on rank only.
        """

        return self.rank == other.rank

    def __lt__(self, other):
        """Less Than. Based on rank only.
        """

        return self.rank < other.rank

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

    def __persist__(self):
        return self.serialize(snoop=True)

    def __repr__(self):
        return ("Card(rank=%s, suit=%s, serialize=%s) @ %s" %
                    (self.rank, self.suit, self.serialize(snoop=True),
                     hex(id(self))))


# Cards Collection
# ================
class Cards(list):
    """ A list of ``Card``s
    """

    def __init__(self, deal_idx=0):
        """
        params
        ------
        deal_idx    (int)   0 or -1 indicating dealing from the top or
                            bottom respectively.
        """
        list.__init__(self)
        self.initlen = 0

        assert deal_idx == 0 or deal_idx == -1, "`deal_idx` must be 0 or -1."
        self._deal_idx = deal_idx

    def __int__(self):
        """Sum all the cards in the list.
        """
        return sum(int(val) for val in self)

    def diff_check(self, threshold):
        """
        diff_check(1.0) to determine if the deck has changed at all.
        diff_check(0.0) to determine if the deck is empty.
        """
        return len(self) <= self.initlen * threshold

    def build(self, numdecks=1, card_cls=Card, deck_type=DeckTypeStandard,
              do_shuffle=False):
        """Build a  ``deck`` or Shoe.
        """
        deck_type = inspect.isclass(deck_type) and deck_type() or deck_type
        for _ in range(numdecks):
            for suit, rank in deck_type.build():
                self.append(card_cls(suit, rank, deck_type=deck_type))

        assert all(map(lambda obj: isinstance(obj, card_cls), self)), ("This "
            "cards list may not contain mixed `card_cls` types.")

        self.initlen = len(self)
        if do_shuffle is True:
            return shuffle(self)
        else:
            return self

    def shuffle(self):
        """
        """
        return shuffle(self)

    def deal(self, target, flip=False, up=None):
        """Deal a card from the ``deck`` to the ``target``.
        """
        
        try:
            card = self.pop(self._deal_idx)
        except IndexError:
            raise DeckEmpty("Cannot deal from an empty deck.")
        else:
            if flip is True:
                card.up = not card.up
            if up is not None:
                card.up = up
            target.append(card)

    def deal_n(self, target, n, **kwa):
        for _ in range(n):
            self.deal(target, **kwa)

    def discard(self, target, **kwa):
        while True:
            try:
                self.deal(target, **kwa)
            except DeckEmpty:
                break

    def __repr__(self):
        return "Cards(%s) @ %s" % (','.join(bicycle.marshal.marshal_object(self, persist=True)),
                                   hex(id(self)))


# (c) 2011-2014 StudioCoda & Nicholas Long. All Rights Reserved