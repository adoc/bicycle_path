from . import Test as TestTables
from cards.blackjack import Card, Shoe
from ..blackjack import Player, Hand, Seat, Table

class Test(TestTables):
    Card = Card
    Shoe = Shoe    
    Player = Player
    Hand = Hand
    Seat = Seat
    Table = Table

    def seat(self):
        s = self.Shoe()
        p1 = self.Player('player1',32000)
        s1 = self.Seat(p1)
        s1.bet(100)
        s1.deal(s.pop())
        s1.deal(s.pop())   
        print s1
        assert s1.hand.pair
        s1.split([s.pop(),s.pop()])
        print s1
        assert s1.hand.pair
        s1.split([s.pop(),s.pop()])
        s1.handidx=1 #Switch to hand with pair.
        print s1
        assert s1.hand.pair
        s1.split([s.pop(),s.pop()])
        print s1
        print s1.actablehands

        for hand in s1.actablehands:
            hand.append(s.pop())

        print s1
        print s1.actablehands
        '''
        s1.nexthand()
        s1.deal(s.pop())
        s1.nexthand()
        s1.deal(s.pop())

        s1.split()

        s1.nexthand()
        s1.deal(s.pop())
        s1.nexthand()
        s1.deal(s.pop())
        '''

        #s1.deal(s.pop())
        
        #s1.split()

        '''
        s1.nexthand()
        s1.deal(s.pop())
        s1.nexthand()
        s1.deal(s.pop())
        '''
        

    def __init__(self):
        super(Test,self).__init__()

        print type(self.Card())
        print type(self.Shoe())
        print type(self.Player())
        print type(self.Hand())
        print type(self.Seat())
        print type(self.Table())

        self.seat()