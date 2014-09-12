from .. import cards
import random, string, itertools

from codalib.data.util import randstr

dealer_name = ['Melvin','Harry','Melinda','Chuck','Sol','Larry','Jerry','Jacky','Johnny',]

#def randstr(length):
#    return ''.join(random.sample((string.ascii_letters + string.digits),length))

class Player(object):
    """ Player object. """

    def __init__(self,name='player',bankroll=0, dealer=False):
        self.id = randstr(16)
        self.name = name
        self.bankroll = bankroll
        self.dealer = dealer

    def serialize(self):
        return {'name':self.name,'bankroll':self.bankroll,'dealer':self.dealer}

    def deserialize(self,dic):
        self.name = dic['name']
        self.bankroll = dic['bankroll']
        self.dealer = dic['dealer']

    def __eq__(self,other):
        if isinstance(other,Player):
            return self.id == other.id
        else:
            #print type(other)
            #print "Other not instance of Player"
            return False

    def __repr__(self):
        return "Player(id=%s,name='%s',bankroll=%s)"%(self.id,self.name,self.bankroll)

class Human(Player):
    pass

class Ai(Player):
    pass

class Hand(list):
    """ A list of Card()s """
    Card = cards.Card
    def __init__(self,cards=None,bet=0):
        if cards:
            for card in cards:
                assert isinstance(card,self.Card)
                self.append(card)
        self.bet = bet
    '''
    def serialize(self):
        """ provides serialization to the class. for json encoding. """
        return [card.__repr__() for card in self]
    '''
    def __repr__(self):
        return "Hand(%s,bet=%s)"%(self[:],self.bet) #[card for card in self]


class Seat(object):
    """ Keeps a list of Hands. """
    Card = cards.Card
    Player = Player
    Hand = Hand
    player = None   

    def __init__(self,player=None):
        if player:
            assert type(player)==self.Player
            self.player = player

        self.hands = [self.Hand()]

    
    def __hand(self):   return self.hands[0]

    hand = property(__hand)

    def __isempty(self):  return self.player == None

    isempty = property(__isempty)

    def __isdealer(self): return self.player.dealer
    
    isdealer = property(__isdealer)

    def __ishuman(self):  return type(self.player)==Human

    ishuman = property(__ishuman)

    def __isai(self):     return type(self.player)==Ai

    ai = property(__isai)

    def __repr__(self):
        if self.player:
            return '"%s" | Bank: %s | Hand(s): %s'%(self.player.name,self.player.bankroll,self.hands)
        else:
            return "Empty Seat"

    '''
    def deal(self,card):
        #print "%s | %s"%(type(self.Card()),type(card))
        assert type(card)==self.Card
        self.hand.append(card)

    def bet(self,bet):
        """ Place bet. """
        assert type(bet)==int
        self.hand.bet += bet
    '''
    
'''
class Seat(object):
    """ Keeps a list of Hands and a list of Bets at this Seat. """
    Card = cards.Card
    Player = Player
    Hand = Hand
    player = None

    def __init__(self, player=None):
        if player:
            assert type(player)==type(self.Player())
            self.player = player

        self.clear()

        #self.__betlist = []
        #self.__handlist = []
        #self.addhand()
        #self.__betcycle = itertools.chain(self.__betlist)
        self.__handcycle = itertools.cycle(self.__handlist)
        self.nexthand()

    def clear(self):
        #self.__betlist = []
        self.__handlist = []
        self.addhand()        

    def nexthand(self):
        self.__handcurrent = self.__handcycle.next()

    def deal(self,card):
        print "%s | %s"%(type(self.Card()),type(card))

        assert type(card)==type(self.Card())
        #if not hasattr(self,'_Seat__handcycle'):
        #    self.__handcycle = itertools.cycle(self.__handlist)
        
        #self.__handcurrent = self.__handcycle.next()
        self.__handcurrent.append(card)

    def bet(self,bet):
        """ Place bet. """
        assert bet>0
        #if not hasattr(self,'_Seat__handcycle'):
        #    self.__handcycle = itertools.cycle(self.__handlist)

        #self.__handcurrent = self.__handcycle.next()
        self.__handcurrent.bet = bet



    def addhand(self,bet=0):
        #self.__betlist.append(bet)
        self.__handlist.append(self.Hand(bet))
        #self.__betcycle = itertools.cycle(self.__betlist)
        #self.__handcycle = itertools.cycle(self.__handlist)

    def __handget(self):
        return self.__handcurrent

    hand = property(__handget)

    def __empty(self):
        return self.player == None

    empty = property(__empty)

    def __repr__(self):
        if self.player:
            return '"%s" | Bank: %s | Hand(s): %s'%(self.player.name,self.player.bankroll,self.__handlist)
        else:
            return "Empty Seat"
'''
'''
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
'''


class Table(object):
    Seat = Seat
    Player = Player
    Shoe = cards.Shoe

    dealingseats = []

    __numseats = 6
    __numdecks = 1

    def __init__(self):
        self.__seats = [self.Seat() for _ in range(self.__numseats)]
        self.shoe = self.Shoe(self.__numdecks)        

    def sit(self,player,seatidx=None):
        seat = None
        if -1 <= seatidx < len(self.__seats):
            seat = self.__seats[seatidx]

        if not seat or not seat in self.__openseats():
            seat = self.__randseat()

        seat.player = player

    def unsit(self,player,seatidx=None):
        """ Removes the player from a [seat] or all seats the player posses. """

        def checkclear(seat):
            if not seat in self.dealingseats:
                self.__seats[self.__seats.index(seat)] = self.Seat()

        seat = None

        player_seats = self.__playerseats(player)

        #print "playerseats: %s"%player_seats

        if -1 < seatidx < len(self.__seats):
            seat = self.__seats[seatidx]
            print "seat: %s"%seat

        if seat in player_seats:
            checkclear(seat)
        elif not seat:
            for seat in player_seats:
                checkclear(seat)

    def bet(self,amount,player,idx=0):
        assert amount >= 0
        seat = self.__playerseats(player)[idx]

        if seat.player.bankroll>=amount:
            seat.player.bankroll-=amount

            

            seat.hand.bet += amount

            assert seat.hand.bet >= 0
            '''
            if seat.hand.bet < 0:
                seat.hand.bet -= amount
                return False
            '''

            return seat.player

    def setdeal(self):
        self.dealingseats = self.bettingseats
        self.__dealingidx = -1

        #self.__dealingseats_cycle = itertools.cycle(self.dealingseats)

        #self.dealing = self.__dealingseats_cycle.next()

        self.nextdeal()

    def dealall(self,numcards=1):
        if self.dealingseats:
            for _ in range(numcards):
                for seat in self.dealingseats:
                    self.deal()
                    self.nextdeal()

    def deal(self,up=False):
        card = self.shoe.pop()
        card.up = up
        self.dealing.hand.append(card)

    def nextdeal(self):
        self.__dealingidx += 1
        if self.__dealingidx >= len(self.dealingseats):
            self.__dealingidx = 0

        self.dealing = self.dealingseats[self.__dealingidx]

        #self.dealing = self.__dealingseats_cycle.next()

    def playerhand(self,player,idx=0,copy=False):
        playerseats = self.__playerseats(player)
        #print "player in question: %s | Seats: %s"%(player,playerseats)
         
        if playerseats:

            if copy:

                sourcehand = playerseats[idx].hand[:]

                for card in sourcehand:
                    card.private = False

                return sourcehand
            else:
                return playerseats[idx].hand

    def clear(self):
        self.cleardealing()
        self.clearhands()

    def cleardealing(self):
        self.dealingseats = []

    def clearhands(self):
        [seat.__init__() for seat in self.__seats]

    def __players(self):
        """ Lists all seats (returns only the Players at the Seat) """
        return [seat.player for seat in self.__seats]

    players = property(__players)

    def __playersbets(self):
        return [seat.hand.bet for seat in self.__seats]

    playersbets = property(__playersbets)

    def __dealingplayers(self):
        """ Lists all the seats being dealt (returns only the Players at the Seat) """
        return [seat.player for seat in self.__seats if seat in self.dealingseats]

    dealingplayers = property(__dealingplayers)

    def __playerseats(self,player):
        """List of seats the [player] controls."""
        #print player
        #return [seat for seat in self.__seats if seat.player and seat.player.id==player.id]
        l = []
        for seat in self.__seats:
            #print "%s == %s??"%(player,seat.player)
            if seat.player==player:
                l.append(seat)
        return l
        #return [seat for seat in self.__seats if seat.player==player]

    def __humanseats(self):
        return [seat for seat in self.__seats if seat.human]

    humanseats = property(__humanseats)

    def __readyseats(self):
        """List of seats that are ready (have a non-dealer player)"""
        return [seat for seat in self.__seats if not seat.isempty and not seat.isdealer]

    readyseats = property(__readyseats)

    def __bettingseats(self):
        return [seat for seat in self.readyseats if seat.hand.bet > 0]

    bettingseats = property(__bettingseats)

    def __bettingplayers(self):
        return [seat.player for seat in self.readyseats if seat.hand.bet > 0]

    bettingplayers = property(__bettingplayers)

   
    def __openseats(self):
        """List of open seats"""
        return [seat for seat in self.__seats if seat.isempty]

    def __randseat(self):
        """Return a random open seat."""
        return random.choice(self.__openseats())

    def __hands(self):
        return [(seat.hand,int(seat.hand)) for seat in self.__seats ] #dealingseats]
    hands = property(__hands)

    def __repr__(self):
        return repr(self.__seats)

class TableGame(object):
    pass


'''
class broken__Table(object):
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

    __seats = [Seat() for _ in range(__numseats)]
    __dealingseats = None
    __dealingseats_cycle = itertools.cycle(dealingseats)

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

    # Tablegame or Game class.
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

    # Tablegame or Game class??
    def bet(self,amount,player=None,idx=0):
        if not player:  player = self.dealing.player
            
        if player.bankroll>=amount:
            player.bankroll-=amount
            seat = self.__playerseats(player)[idx]

            #seat.bet = seat.bet + amount
            seat.bet += amount
            return True





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







"""
Seat Class
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