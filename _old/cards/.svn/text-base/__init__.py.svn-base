'''__init__.py
Version: 1.0b (0.7)
Author:  Nathan Beste
         Nicholas Long
Date: 2010-06-12
Revisions:
    2010-06-28:  NL - Abstracted classes. Moved in to module cards.py as base card classes for re-use.
    2010-06-29:  NL - Card() Added __eq__ comparer and "wildcard" functionality.
                      Hand() Added find() method for finding cards in a hand.
    2011-05-24:  NL - moved to __init__.
                      cleaned up classes a bit.
(c) 2011 StudioCoda & Nicholas Long. All Rights Reserved'''
from random import shuffle

Suits = ['S','C','H','D']

class _Ranks(object):
    """ Card Ranks.
        Usage:
            Ranks[] is a list of string card rank representations.
            Index starts at 1."""
    _ranks = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
    def __len__(self):
        return len(self._ranks)
    def __iter__(self): 
        for rank in self._ranks:
            yield rank
    def __getitem__(self,rank):
        return self._ranks[rank-1]
    def index(self,index):
        return self._ranks.index(index)+1

Ranks = _Ranks()

class Card(object):
    """ A Lonely Card.
          Usage:
            Card('2C')
            Card([suit=index],[rank=index]) """
    private = True
    up = False
    rank = -1
    suit = -1
    def __init__(self,*args,**kwargs):
        """ 
        args([cardstring] or [Card]):
            cardstring:
            Card:

        kwargs([suit],[rank],[up]):

        """
        #rank = -1
        #suit = -1
        if len(args):
            if isinstance(args[0],str):
                if len(args[0])==1:
                    self.rank = Ranks.index(args[0].upper()[0])
                if len(args[0])==2:
                    self.rank = Ranks.index(args[0].upper()[0])
                    self.suit = Suits.index(args[0].upper()[1])
            elif isinstance(args[0],Card): #"cast"
                self.__dict__.update(args[0].__dict__)
                '''
                self.rank = args[0].rank
                self.suit = args[0].suit
                self.up = args[0].up
                self.private = args[0].private
                '''

        if isinstance(kwargs.get('suit'),str):
            self.suit = Suits.index(kwargs['suit'].upper())
        elif isinstance(kwargs.get('suit'),int):
            self.suit = kwargs['suit']

        if isinstance(kwargs.get('rank'),str):
            self.rank = Ranks.index(kwargs['rank'].upper())
        elif isinstance(kwargs.get('rank'),int):
            self.rank = kwargs['rank']

        if kwargs.get('up'):
            self.up = kwargs['up']

    def __eq__(self,other):
        return (self.suit < 0 or other.suit < 0 or self.suit == other.suit) and (self.rank < 0 or other.rank < 0 or self.rank == other.rank)

    def __iter__(self):
        yield self.suit
        yield self.rank

    def serialize(self):
        if self.private and not self.up:
            rank = 'X'
            suit = 'X'
        else:
            rank = Ranks[self.rank] if self.rank >= 0 else '*'
            suit = Suits[self.suit] if self.suit >= 0 else '*'

        return "%s%s"%(rank,suit)       

    def __repr__(self): # String templating instead of concatenation
        return "%s%s%s"%(Ranks[self.rank] if self.rank >= 0 else '*',Suits[self.suit] if self.suit >= 0 else '*',not self.up and 'X' or '')

class Deck(list):
    """ A Deck of Cards.
        Usage:
            Deck() - Build a Deck of 52 cards of type Card()"""
    Suits = Suits
    Ranks = Ranks
    Card = Card
    def __init__(self):
        for suit in self.Suits:
            for rank in self.Ranks:
                self.append(self.Card(suit=suit,rank=rank))
        self.initlen = len(self)
    def __repr__(self):
        string = ''
        for card in self:
          string = '%s%s,'%(string,repr(card))
        return string[:-1]

    def shuffle(self):
        shuffle(self)

    def check(self,factor=1):
        return len(self) < factor*self.initlen

    def serialize(self):
        """ provides serialization to the class. for json encoding. """
        return [card.__repr__() for card in self]

class Shoe(Deck):
    """ A Shoe of Decks. 
        Usage:
            Shoe(numdecks=1)"""
    def __init__(self,numdecks=1):
        self.numdecks=numdecks
        for _ in range(numdecks):
            super(Shoe,self).__init__()        

    def reset(self):
        self.__init__(self.numdecks)

# (c) 2011 StudioCoda & Nicholas Long. All Rights Reserved