import bicycle.cards


class Card(bicycle.cards.Card):
    """
    """

    def __int__(self):
        """
        """

        if self.rank < 9: # A thru 9 return value
          return self.rank + 1

        elif self.rank <= 12: # 10, J, Q, K return 10
          return 10

    def __eq__(self, other):
        """
        """
        # matches value
        return int(self) == int(other)


Ace = Card.from_str('AS')


class Hand(bicycle.cards.Hand):
    """
    """

    def __int__(self):
        """
        """
        s = sum(int(val) for val in self)

        if s <= 11 and Ace in self:
            s += 10

        return s


# Deck of blackjack cards. Might make this a class instead.
Deck = lambda **kwa: bicycle.cards.Deck(card_cls=Card, **kwa)


# Shoe of blackjack cards.
Shoe = lambda **kwa: bicycle.cards.Shoe(card_cls=Card, **kwa)




# (c) 2011-2014 StudioCoda & Nicholas Long. All Rights Reserved