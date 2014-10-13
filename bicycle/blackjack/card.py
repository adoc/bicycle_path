"""Blackjack Cards Module
"""

import functools
import bicycle.card


@functools.total_ordering
class Card(bicycle.card.Card):
    """A Blackjack card, including equivalence
    """

    def __int__(self):
        """Cast to integer. A to 10 return blackjack rank value
        (i.e. 1 through 10); J, Q, K all return 10.
        """

        return min([self.rank + 1, 10])

    def __eq__(self, other):
        """Equivalence; Matches integer value.
        """

        return int(self) == int(other)

    def __lt__(self, other):
        """Less Than; Matches less than integer value.
        """

        return int(self) < int(other)


ace = Card.from_str('AS')


#@functools.total_ordering
class Hand(bicycle.card.Cards):
    """
    """

    @property
    def blackjack(self):
        """The hand is a blackjack.
        """

        return len(self) == 2 and self.__int__(snoop=True) == 21

    @property
    def busted(self):
        """The hand is busted.
        """

        return self.__int__(snoop=True) > 21

    @property
    def soft(self):
        """The hand is soft; has an ace.
        """
        return bicycle.card.Cards.__int__(self) <= 11 and ace in self
        #return ace in self  # Nope, this isn't soft. Soft is where the
                            # ace is acting like an 11.

    @property
    def splittable(self):
        """The hand is splittable.
        """

        return len(self) == 2 and self[0].rank == self[1].rank

    @property
    def stop(self):
        """All player actions stop on this Hand.
        """

        return self.__int__(snoop=True) >= 21

    @staticmethod
    def quant(hand):
        return (hand.busted is not True and hand.__int__(snoop=True) or 0 + 
                hand.blackjack is True and 1 or 0)

    def __eq__(self, other):
        return self.quant(self) == self.quant(other)

    def __gt__(self, other):
        return self.quant(self) > self.quant(other)

    def __lt__(self, other):
        return self.quant(self) < self.quant(other)

    def __int__(self, snoop=False):
        """
        * int is not used to quantify the hand for comparison. This
        might be changed.
        """
        s = bicycle.card.Cards.__int__(self, snoop)

        if s <= 11 and ace in self:
            s += 10

        return s


# (c) 2011-2014 StudioCoda & Nicholas Long. All Rights Reserved