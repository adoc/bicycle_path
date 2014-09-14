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

    def __eq__(self,other):
        """
        """
        # matches value
        return int(self) == int(other)


# Deck of blackjack cards.
Deck = lambda **kwa: bicycle.cards.Deck(card_cls=Card, **kwa)

# Shoe of blackjack cards.
Shoe = lambda **kwa: bicycle.cards.Shoe(card_cls=Card, **kwa)


# (c) 2011-2014 StudioCoda & Nicholas Long. All Rights Reserved