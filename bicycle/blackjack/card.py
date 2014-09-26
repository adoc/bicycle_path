"""Blackjack Cards Module
"""

import functools
import bicycle.cards


@functools.total_ordering
class Card(bicycle.cards.Card):
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


class Hand(bicycle.cards.Cards):
    """
    """

    def __int__(self):
        """
        """
        s = sum(int(val) for val in self)

        if s <= 11 and ace in self:
            s += 10

        return s

    @property
    def blackjack(self):
        """
        """

        return len(self) == 2 and int(self) == 21


build = functools.partial(bicycle.cards.build, card_cls=Card)


# (c) 2011-2014 StudioCoda & Nicholas Long. All Rights Reserved