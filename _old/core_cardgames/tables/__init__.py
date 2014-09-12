import cards, random, itertools

dealer_name = ['Melvin','Harry','Melinda','Chuck','Sol','Larry','Jerry','Jacky','Johnny',]

class Player(object):
    """ Player object. """
    def __init__(self,name='player',bankroll=0):
        self.name = name
        self.bankroll = bankroll

    def __repr__(self):
        return "Player(name='%s',bankroll=%s)"%(self.name,self.bankroll)


class Hand(list):
    """ A list of Card()s """
    Card = cards.Card
    def __init__(self,cards=None,bet=0):
        if cards:
            for card in cards:
                assert type(card)==self.Card
                self.append(card)
        self.bet = bet

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
        #self.handidx = 0

    '''
    def __gethand(self):
        return self.hands[self.handidx]

    hand = property(__gethand)

    def deal(self,card):
        #print "%s | %s"%(type(self.Card()),type(card))
        assert type(card)==self.Card
        self.hand.append(card)

    def bet(self,bet):
        """ Place bet. """
        assert type(bet)==int
        self.hand.bet += bet
    '''


    def __empty(self):
        return self.player == None

    empty = property(__empty)

    def __repr__(self):
        if self.player:
            return '"%s" | Bank: %s | Hand(s): %s'%(self.player.name,self.player.bankroll,self.hands)
        else:
            return "Empty Seat"
    
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

    __numseats = 6
    __numdecks = 1

    __seats = [Seat() for _ in range(__numseats)]
    __shoe = Shoe(__numdecks)

    def sit(self,player,seat=None):
        if not seat or not seat in self.__openseats():
            seat = self.__randseat()
        seat.player = player

    def unsit(self,player,seat=None):
        """ Removes the player from a [seat] or all seats the player posses. """
        player_seats = self.__playerseats(player)

        if seat in player_seats:
            seat.player = None
            seat.inithand()
        elif not seat:
            for seat in player_seats:
                seat.__init__()


    def __playerseats(self,player):
        """List of seats the [player] controls."""
        return [seat for seat in self.__seats if seat.player==player]

    def __readyseats(self):
        """List of seats that are ready (have a player)"""
        return [seat for seat in self.__seats if not seat.empty]

    def __openseats(self):
        """List of open seats"""
        return [seat for seat in self.__seats if seat.empty]

    def __randseat(self):
        """Return a random open seat."""
        return random.choice(self.__openseats())

    def __repr__(self):
        return repr(self.seats)

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