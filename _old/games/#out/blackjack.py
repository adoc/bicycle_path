import games, random

from cards.blackjack import Shoe, Card
from strategy.blackjack import PlayerStrategy, DealerStrategy




dealer_name = ['Constantine','Melvin','Harry','Melinda','Chuck','Sol','Larry','Jerry','Jacky','Johnny',]

class Table(games.Table):
    """ """
    Seat = Seat
    Player = Player
    Shoe = Shoe

    def __init__(self, numseats=7, numdecks=6):
        super(Table,self).__init__(numseats,numdecks)

    def checkhand(self):
        if self.dealing.hand.busted:
            self.loss()
            self.nextdeal()

    def clearhand(self):
        self.dealing.inithand()
        #print "%s init hand (%s)"%(self.dealing.player.name,self.dealing.hand)

    def loss(self):
        self.dealer.player.bankroll += self.dealing.bet

    def win(self):
        print "winner: %s"%self.dealing.bet
        self.dealer.player.bankroll -= self.dealing.bet
        self.dealing.player.bankroll += 2*self.dealing.bet

    def push(self):
        self.dealing.player.bankroll += self.dealing.bet

    def resolve(self):
        """ Finish the round. Resolve bets. Clear the table. """
        if self.dealer in self.dealingseats:
            #self.dealingseats.remove(self.dealer)
            
            dealer_total = int(self.dealer.hand)
            self.dealing = self.dealer

            for seat in self.dealingseats[:]:
                
                self.dealing = seat
                seat_total = int(seat.hand)

                if seat_total<dealer_total:
                    self.loss()
                elif seat_total==dealer_total:
                    self.push()
                elif seat_total>dealer_total:
                    self.win()

                print "resolving: %s"%seat
                self.clearhand()

        else:
            for seat in self.dealingseats[:]:
                self.dealing = seat
                self.win()

    def data(self):
        #if int(self.dealing.hand)>0:
        return [self.dealing,self.dealer.hand[1]]

    def __double(self):
        if len(self.dealing.hand)==2:
            if super(Table,self).bet(self.dealing.bet): #,self.dealing.player):
                self.dealing.hand.stand=True
        
    def doublestand(self):
        self.__double()
        self.stand()
        
    def doublehit(self):
        self.__double()
        self.hit()

    def split(self):
        print "IMPLEMENT SPLIT!!!"
        self.hit()

    def hit(self):
        self.deal()

    def stand(self):
        self.dealing.hand.stand=True

    
    def act(self,action):
        if action=="S":
            self.stand()
        elif action=="H":
            self.hit()
        elif action=="Hd":
            self.doublehit()
        elif action=="Hu":
            self.hit()
        elif action=="P":
            self.split()
        elif action=="Sd":
            self.doublestand()



    def __readyseats(self):
        return [seat for seat in self.seats if (seat.player!=None and seat.bet > 0) or seat==self.seats[-1]]

'''
class Game(object):
    def __init__(self, table=Table):
        self.table = table()
        self.ps = PlayerStrategy()
        self.ds = DealerStrategy()
        

    def strat2act(self,action):
        if action=="S":
            self.table.stand()
        elif action=="H":
            self.table.hit()
        elif action=="Hd":
            self.table.doublehit()
        elif action=="Hu":
            self.table.hit()
        elif action=="P":
            self.table.split()
        elif action=="Sd":
            self.table.doublestand()
'''