from .. import cards

Ranks = cards.Ranks
Suits = cards.Suits

class Card(cards.Card):
    def __int__(self):
        if 0 < self.rank < 10: # A thru 9 return value
          return self.rank
        if 10 <= self.rank < 14: # 10, J, Q, K return 10
          return 10

    def __eq__(self,other):
        """ matches value """
        return self.rank<0 or other.rank<0 or self.__int__() == int(other)

class ShowCard(Card):
    def __int__(self):
        if self.up: #or not self.private:
            return super(ShowCard,self).__int__()
        else:
            return -10

class Deck(cards.Deck):
    Suits = Suits
    Ranks = Ranks
    Card = Card
    """Overloads cards.Deck to use blackjack.Card"""

class Shoe(cards.Shoe,Deck):
    """Overloads cards.Shoe and blackjack.Deck"""
    pass

# (c) 2011 StudioCoda & Nicholas Long. All Rights Reserved