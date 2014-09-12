import random, itertools, cards
from cards import Shoe

'''
class Player(object):
    """ Player object.
    """
    def __init__(self,name='player',bankroll=0):
        self.name = name
        self.bankroll = bankroll

    def __repr__(self):
        return "Player(name='%s',bankroll=%s)"%(self.name,self.bankroll)

class Hand(list):
    """ A list of Card()s """
    def __repr__(self):
        return "%s"%[card for card in self]

class Seat(object):
    """
    player      - Player object.
    bet         - Bet value.
    hand        - Current playing hand.
    empty       - Seat has no player.
    numhands    - Number of hands at this seat.
    addhand()   -
    nexthand()  - Deals to the next hand.

    __handtype      - Type of Hand to use. Default (games.Hand)
    __handlist      -
    __handcycle     -
    __handcurrent   -
    """
    def __init__(self,handtype=Hand):
        self.__handtype = handtype
        self.player = None
        #self.bet = 0
        self.inithand()

    def inithand(self):
        self.__betlist = []
        self.__handlist = []
        self.addhand()
        self.nexthand()

    def addhand(self,bet=0):
        self.__betlist.append(bet)
        self.__handlist.append(self.__handtype())
        self.__betcycle = itertools.cycle(self.__betlist)
        self.__handcycle = itertools.cycle(self.__handlist)

    def nexthand(self):
        self.__betcurrent = self.__betcycle.next()
        self.__handcurrent = self.__handcycle.next()

    def __handget(self):
        return self.__handcurrent
    
    hand = property(__handget)

    def __betget(self):
        return self.__betcurrent

    def __betset(self,bet):
        self.__betcurrent = bet

    bet = property(__betget,__betset)

    def __empty(self):
        return self.player == None

    empty = property(__empty)

    def __repr__(self):
        if self.player:
            return '"%s" | Bank: %s | Bet: %s | Hand(s): %s'%(self.player.name,self.player.bankroll,self.bet,self.__handlist)
        else:
            return "Empty Seat"
'''

dealer_name = ['Melvin','Harry','Melinda','Chuck','Sol','Larry','Jerry','Jacky','Johnny',]

'''
class Table(object):
    """
    Base Table Class.

    Implements:
        checkshoe   - Implements Shoe.check(factor=1), resets the cards and shuffles if any cards have been dealt.
        setdeal     - Sets the list of players being dealt.
        newdeal     - Deals a [numcards] of cards to players.
        deal        - Deals a single card to the current player.
        nextdeal    - Next deal to next player.
        bet
        sit
        resolvebets
        clear
        clearcards
        clearbets
        isdealer
        *playerseats
        __readyseats
        __openseats
        __randseats
    """
    Seat = Seat
    Player = Player
    Shoe = Shoe
    def __init__(self, numseats=6, numdecks=1):
        self.seats = [self.Seat() for i in range(numseats)]
        self.dealingseats = None
        self.dealing = None
        self.dealer = self.sit(self.Player(random.choice(dealer_name),bankroll=1000000), self.seats[-1])
        self.shoe = self.Shoe(numdecks)

    def checkshoe(self,factor=1):
        if self.shoe.check(factor):
            self.shoe.reset()
            self.shoe.shuffle()

    def setdeal(self):
        self.dealingseats = self.__readyseats()
        self.dealingseats_cycle = itertools.cycle(self.dealingseats)
        self.dealing = self.dealingseats_cycle.next()

    def newdeal(self,numcards=5):
        if self.dealingseats:
            for _ in range(numcards):
                for seat in self.dealingseats:
                    self.deal()
                    last = self.nextdeal()
            #return last

    def deal(self):
        self.dealing.hand.append(self.shoe.pop())

    def nextdeal(self):
        self.dealing = self.dealingseats_cycle.next()
        #return self.dealing

    def bet(self,amount,player=None,idx=0):
        if not player:  player = self.dealing.player
            
        if player.bankroll>=amount:
            player.bankroll-=amount
            seat = self.__playerseats(player)[idx]

            #seat.bet = seat.bet + amount
            seat.bet += amount
            return True

    def sit(self,player,seat=None):
        if not seat or not seat in self.__openseats():
            seat = self.__randseat()
        seat.player = player
        return seat

    def unsit(self,player,seat=None):
        """ Removes the player from a [seat] or all seats the player posses. """
        player_seats = self.__playerseats(player)
        if seat in player_seats:
            seat.player = None
            seat.inithand()
        else:
            for seat in player_seats:
                seat.player = None
                seat.inithand()

    def __playerseats(self,player):
        """List of seats the [player] controls."""
        return [seat for seat in self.seats if seat.player==player]

    def __readyseats(self):
        """List of seats that are ready (have a player)"""
        return [seat for seat in self.seats if seat.player!=None]

    def __openseats(self):
        """List of open seats"""
        return [seat for seat in self.seats if seat.empty]

    def __randseat(self):
        """Return a random open seat."""
        return random.choice(self.__openseats())

    def __repr__(self):
        return repr(self.seats)
        #return 'Dealer: %s | Dealing%s | Seats: %s'%(self.dealer,self.dealing,self.seats)
'''