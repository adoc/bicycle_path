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


class Hand(bicycle.card.Cards):
    """
    """

    def __int__(self, snoop=False):
        """
        """
        s = bicycle.card.Cards.__int__(self, snoop)

        if s <= 11 and ace in self:
            s += 10

        return s

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


# (c) 2011-2014 StudioCoda & Nicholas Long. All Rights Reserved