import tables
import cards.blackjack

class Player(tables.Player):
    pass

class Hand(tables.Hand):
    Card = cards.blackjack.Card
  
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

    def __actable(self): return not self.busted and not self.twentyone and not self.stand
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
    '''

    def __repr__(self):
        #return "%s (%i) | %s | %s | %s "%([card for card in self],self,self.busted,self.twentyone,self.stand)
        return "%s (%i)"%([card for card in self],self)

class Seat(tables.Seat):
    Card = cards.blackjack.Card
    Player = Player
    Hand = Hand

    def split(self,hand,cards):
        card = hand.split()
        hand.append(cards[0])
        self.hands.append(self.Hand([card,cards[1]]))


    def __actablehands(self):
        return [hand for hand in self.hands if hand.actable]

    actablehands = property(__actablehands)

    def __actable(self):
        return len(self.actablehands) > 0

    actable = property(__actable)




        #card = self.hand.split()
        #self.addhand()
        #self.nexthand()
        #self.deal(card)
        


class Table(tables.Table):
    pass