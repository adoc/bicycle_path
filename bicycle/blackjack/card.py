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

    def __lt__(self, other):
        """Less Than; Matches less than integer value.
        """

        return int(self) < int(other)

    def __eq__(self, other):
        """Equivalence; Matches integer value.
        """

        return int(self) == int(other)


ace = Card.from_str('AS')


class Hand(bicycle.card.Cards):
    """
    """

    def __int__(self):
        """
        """
        s = bicycle.card.Cards.__int__(self)

        if s <= 11 and ace in self:
            s += 10

        return s

    @property
    def blackjack(self):
        """The hand is a blackjack.
        """

        return len(self) == 2 and int(self) == 21

    @property
    def busted(self):
        """The hand is busted.
        """

        return int(self) > 21

    @property
    def soft(self):
        """The hand is soft; has an ace.
        """

        return ace in self

    @property
    def stop(self):
        """All player actions stop on this Hand.
        """

        return int(self) >= 21

    # Do we do "bust", "splitable", etc here??


# (c) 2011-2014 StudioCoda & Nicholas Long. All Rights Reserved