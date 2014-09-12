import logging
log = logging.getLogger(__name__)

from ..tables import Table, Player, Hand

from codalib.data.util import randstr

class GameStep(object):
    timeout = 5
    desc = "GameStep"
    def __init__(self,table):
        log.debug("Gamestep table type: %s"%type(table))
        #print "Gamestep table type: %s"%type(table)
        assert isinstance(table,Table)
        self.table = table

    def evaluate(self):
        pass

    def do(self):
        pass

    def data(self,*args):
        #print "GameStep.data(%s)"%args

        bet = 0
        ret = {}
        
        if args:
            player = args[0]
            
            hand = self.table.playerhand(player)
            #print "player: %s | hand: %s"%(player,hand)
            if isinstance(hand,Hand): # hand != None:  works! but not pythonic   #  if hand:  will not work due to an empty hand being []
                ret.update({'bet':hand.bet})

        ret.update({'players':self.table.players,
                'players_bets':self.table.playersbets,
                'dealing':False,})

        return ret

    def bet(self,amount,player,idx=0):
        #if not player:  player = self.table.dealing.player
        return self.table.bet(amount,player,idx)

    def sit(self,player,idx=None):
        assert isinstance(player,Player)
        self.table.sit(player, idx)

    def unsit(self,player,idx=None):
        assert isinstance(player,Player)
        self.table.unsit(player,idx)

class ReadySeatsStep(GameStep):
    timeout = 5
    desc = "ReadySeatsStep"
    def evaluate(self):
        #print "CheckReadySeats() - do()"

        if self.table.shoe.check(factor=.2):
            self.table.shoe.reset()

        if len(self.table.readyseats) > 0:
            return BetsStep

        return ReadySeatsStep            


class BetsStep(ReadySeatsStep):
    timeout = 5
    desc = "BetsStep"
    def evaluate(self):
        if self.table.bettingplayers:
            self.table.setdeal()
            return DealStep        

        return super(BetsStep,self).evaluate()

class DealStep(GameStep):
    timeout = 1
    desc = "DealStep"
    def bet(self,*args):
        return {'message':'Betting is closed.'}

    def data(self,player):
        base = super(DealStep,self).data()
        base.update({'dealingplayers':self.table.dealingplayers})
        if isinstance(player,Player):
            base.update({'hand':self.table.playerhand(player)})

        return base
    
    def evaluate(self):
        if len(self.table.dealingseats[-1].hand) == 5:
            return ResolveStep
        else:
            return DealStep

    def do(self):
        self.table.dealall()

class ResolveStep(GameStep):
    timeout = 5
    desc = "ResolveStep"
    def bet(self,*args):
        return {'message':'Betting is closed.'}

    def evaluate(self):
        return ReadySeatsStep

    def do(self):
        #print "Clearing hands"
        self.table.clear()

