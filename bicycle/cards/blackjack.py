import functools
import bicycle.cards


class Card(bicycle.cards.Card):
    """
    """

    def __int__(self):
        """
        """

        # A to 10 return value; J, Q, K all return 10
        return min([self.rank + 1, 10])


    def __eq__(self, other):
        """
        """
        # matches value
        return int(self) == int(other)


Ace = Card.from_str('AS')


class Hand(bicycle.cards.Cards):
    """
    """

    def __int__(self):
        """
        """
        s = sum(int(val) for val in self)

        if s <= 11 and Ace in self:
            s += 10

        return s



build = functools.partial(bicycle.cards.build, card_cls=Card)


# (c) 2011-2014 StudioCoda & Nicholas Long. All Rights Reserved
