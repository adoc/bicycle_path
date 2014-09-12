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
    def __init__(self,*args,**kwargs):
        rank = -1
        suit = -1
        if len(args):
            if len(args[0])==1:
                rank = Ranks.index(args[0].upper()[0])
            if len(args[0])==2:
                rank = Ranks.index(args[0].upper()[0])
                suit = Suits.index(args[0].upper()[1])

        if type(kwargs.get('suit'))==str:
            suit = Suits.index(kwargs['suit'].upper())
        elif type(kwargs.get('suit'))==int:
            suit = kwargs['suit']

        if type(kwargs.get('rank'))==str:
            rank = Ranks.index(kwargs['rank'].upper())
        elif type(kwargs.get('rank'))==int:
            rank = kwargs['rank']

        self.suit = suit
        self.rank = rank

    def __eq__(self,other):
        '''
        suitmatch = True if self.suit < 0 or other.suit < 0 or self.suit == other.suit else False
        rankmatch = True if self.rank < 0 or other.rank < 0 or self.rank == other.rank else False
        '''
        return (self.suit < 0 or other.suit < 0 or self.suit == other.suit) and (self.rank < 0 or other.rank < 0 or self.rank == other.rank)

        #print self.suit
        #print self.rank

        #return suitmatch and rankmatch

    def __iter__(self): # Allow object to be itterated. i.e. list(self) returns [self.suit, self.rank]
        yield self.suit
        yield self.rank

    def __repr__(self): # String templating instead of concatenation
        return "%s%s"%(Ranks[self.rank] if self.rank >= 0 else '*',Suits[self.suit] if self.suit >= 0 else '*')

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

class Shoe(Deck):
    """ A Shoe of Decks. 
        Usage:
            Shoe(numdecks=1)"""
    def __init__(self,numdecks=1):
        for _ in range(numdecks):
            super(Shoe,self).__init__()
   
    def reset(self):
        self.__init__(self.numdecks)

# (c) 2011 StudioCoda & Nicholas Long. All Rights Reserved