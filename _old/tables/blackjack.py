from .. import tables
from ..cards import blackjack
import random

class Hand(tables.Hand):
    Card = blackjack.Card
  
    def __total(self):
        i = 0
        for h in self:
            i += int(h)
        
        if i<=11 and self.Card('a') in self:
            i += 10

        return i

    def split(self):
        return self.pop()

    def __pair(self):   return self[0] == self[1] and len(self)==2
    def __soft(self):   return self.Card('a') in self and len(self)==2
    def __busted(self): return self.total > 21
    def __twentyone(self):  return self.total == 21
    def __blackjack(self):  return self.total == 21 and len(self)==2

    def __actable(self): return len(self) > 0 and not self.busted and not self.twentyone and not self.stand
    __stand = False
    def __standset(self,value):   self.__stand=value
    def __standget(self):   return self.__stand
    
    total = property(__total)
    busted = property(__busted)
    twentyone = property(__twentyone)
    blackjack = property(__blackjack)
    soft = property(__soft)
    pair = property(__pair)
    stand = property(__standget, __standset)
    actable = property(__actable)

    def __int__(self):  return self.total

    '''
    def clear(self):
        super(Hand,self).clear()
        self.__stand = False

    def __repr__(self):
        #return "%s (%i) | %s | %s | %s "%([card for card in self],self,self.busted,self.twentyone,self.stand)
        return "%s (%i)"%([card for card in self],self)
    '''

class ShowHand(Hand):
    Card = blackjack.ShowCard

    def __init__(self, *args):
        if len(args):
            if isinstance(args[0],Hand):
                self = [self.Card(card) for card in args[0]]


class Seat(tables.Seat):
    Card = blackjack.Card
    Player = tables.Player
    Hand = Hand

    def split(self,hand,cards):
        card = hand.split()
        hand.append(cards[0])
        self.hands.append(self.Hand([card,cards[1]]))


    def __actablehands(self):
        return [hand for hand in self.hands if hand.actable]

    actablehands = property(__actablehands)

    def __actable(self):
        #print "%s | %s"%(self.player,self.actablehands)
        return len(self.actablehands) > 0

    actable = property(__actable)

        #card = self.hand.split()
        #self.addhand()
        #self.nexthand()
        #self.deal(card)
        


class Table(tables.Table):
    Seat = Seat
    Shoe = blackjack.Shoe

    def __init__(self):
        super(Table,self).__init__()
        self.sit(self.Player(random.choice(tables.dealer_name),bankroll=1000000), -1)
        self.shoe.shuffle()

    def dealall(self,numcards=1):
        if self.dealingseats:
            for _ in range(numcards):
                for seat in self.dealingseats:
                    #print "hand len: %s"%len(seat.hand)
                    #print seat==self.__seats[-1]
                    #if not seat==self.__seats[-1] or (seat==self.__seats[-1] and len(seat.hand)>0 ):
                    if seat==self.__seats[-1] and len(seat.hand)>0:
                            
                        self.deal(up=True)
                        #print "dealing up: %s"%seat
                    else:
                        self.deal(up=False)
                        #print "dealing down: %s"%seat
                    self.nextdeal()

    def deal(self,up=False):
        card = self.shoe.pop()
        card.up = up
        self.dealing.hand.append(card)

    def __dealer(self):
        return self.__seats[-1]
    dealer = property(__dealer)

    def __actableseats(self):
        return [seat for seat in self.__seats if seat.actable]

    actableseats = property(__actableseats)

    def __actable(self):
        return len(self.actableseats) > 0

    actable = property(__actable)

    def __bettingseats(self):
        return super(Table,self).__bettingseats() + [self.__seats[-1]]
        #return [seat for seat in self.readyseats if seat.hand.bet > 0]

    bettingseats = property(__bettingseats)