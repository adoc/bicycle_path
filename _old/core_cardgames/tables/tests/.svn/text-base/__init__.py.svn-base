import cards
from .. import Player, Hand, Seat, Table

class Test(object):
    Card = cards.Card
    Shoe = cards.Shoe    
    Player = Player
    Hand = Hand
    Seat = Seat
    Table = Table

    def player(self):
        p1 = self.Player('player1',32000)
        p2 = self.Player('player2',64000)

        assert p1.name == 'player1' and p1.bankroll == 32000
        assert p2.name == 'player2' and p2.bankroll == 64000

    def seat(self):
        s = self.Shoe()

        p1 = self.Player('player1',32000)
        p2 = self.Player('player2',64000)
        
        s1 = self.Seat(p1)
        s2 = self.Seat(p2)
        '''
        s1.addhand()

        s1.bet(100)
        s1.bet(100)

        s2.bet(200)

        s1.deal(s.pop())
        s2.deal(s.pop())
        s1.deal(s.pop())
        s2.deal(s.pop())
        s1.deal(s.pop())
        s2.deal(s.pop())
        s1.deal(s.pop())
        s2.deal(s.pop())
        s1.deal(s.pop())
        s2.deal(s.pop())
        s1.deal(s.pop())
        s2.deal(s.pop())
        '''

        print s1
        print s2

    def __init__(self):
        print type(self.Card())
        print type(self.Shoe())
        print type(self.Player())
        print type(self.Hand())
        print type(self.Seat())
        print type(self.Table())

        # Player test.
        self.player()

        self.seat()

        return None

        s=Shoe()
        s.shuffle()

        p1 = Player('player1')

        
        s1 = Seat(p1)
        

        s1.bet = 100
        s1.hand.append(s.pop())
        s1.hand.append(s.pop())
        s1.hand.append(s.pop())
        
        s1.addhand()
        s1.nexthand()

        s1.hand.append(s.pop())
        s1.hand.append(s.pop())
        s1.hand.append(s.pop())

        print s1


        p2 = Player('player2')

        s2 = Seat(player=p2)

        s2.hand.append(s.pop())
        s2.hand.append(s.pop())
        s2.hand.append(s.pop())


        '''
        print s1.hand
        for card in s1.hand:
            assert type(card)==Card
            assert not card in s
            
        print s2.hand
        for card in s2.hand:
            assert type(card)==Card
            assert not card in s

        table = [Seat() for _ in range(10)]

        for seat in table:
            assert seat.empty
        '''
