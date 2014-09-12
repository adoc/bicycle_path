import logging
log = logging.getLogger(__name__)

from .. import games
from ..tables.blackjack import Table
from ..tables import Player
from ..strategy.blackjack.actors import PlayerActor,DealerActor

from codalib.data.util import randstr

class ReadySeatsStep(games.GameStep):
    timeout = 1
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
    def __init__(self,*args):
        super(BetsStep,self).__init__(*args)

    def evaluate(self):
        if self.table.bettingplayers:
            self.table.setdeal()
            return DealStep        
        else:
            return super(BetsStep,self).evaluate()

class DealStep(games.GameStep):
    timeout = 1
    desc = "DealStep"
    def bet(self,*args):
        return {'message':'Betting is closed.'}

    def data(self,*args):
        #print "blackjack.DealStep.data()"
        base = super(DealStep,self).data(*args)

        base.update({'dealingplayers':self.table.dealingplayers})
        if args:
            #print "args[0]: %s"%args[0]
            player = args[0]
            #print type(player)
            if isinstance(player,Player):
                # ShowCard update...    
                base.update({'hand':self.table.playerhand(player,copy=True)})
                #base.update({'hand':ShowHand(self.table.playerhand(player))})
                base.update({'handtotal':int(self.table.playerhand(player))})
                base.update({'table_hands':self.table.hands})
        return base
    
    def evaluate(self):
        assert len(self.table.dealingseats[-1].hand) <= 2
        if len(self.table.dealingseats[-1].hand) == 2:
            return PlayStep
        else:
            return DealStep

    def do(self):
        self.table.dealall()



class PlayStep(DealStep):
    """ """
    timeout = 10
    desc = "PlayStep"

    def data(self,*args):
        #print "blackjack.PlayStep .data()"
        base = super(PlayStep,self).data(*args)

        if args:
            if args[0]==self.table.dealing.player:
                base.update({'dealing':True})
        return base

    def stand(self,*args):
        if args:
            #print "stand args: %s"%args[0]
            self.table.playerhand(args[0]).stand = True
            #self.do()
            self.evaluate()

    def hit(self,*args):
        print "hit?"
        if args:
            if args[0] == self.table.dealing.player:
                self.table.deal(up=True)
                #self.do()
                self.evaluate()

    # bad bad 
    def evaluate(self):
        print "blackjack.PlayStep.evaluate()"
        if not self.table.dealing.actable:
            self.table.nextdeal()

        if self.table.dealing.actable:
            if self.table.dealing == self.table.dealer and not hasattr(self,'da'):
                self.table.dealing.hand[0].up = True
                self.da = DealerActor(self.table.dealing,self.hit,self.stand)
                self.da.act()
                print "once only"
            else:
                self.pa = PlayerActor(self.table.dealing,int(self.table.dealer.hand[1]),self.hit, self.stand,self.hit,self.stand,self.hit)
                self.pa.start()

        #self.do()

        if self.table.actable:
            return None
        else:
            if hasattr(self,'da'):
                self.da.timer.cancel()
            if hasattr(self,'pa'):
                self.pa.timer.cancel()
            return ResolveStep

    def do(self):
        print "blackjack.PlayStep.do()"

PlayerActor.timeout = PlayStep.timeout

class ResolveStep(PlayStep):
    timeout = 5
    desc = "ResolveStep"

    def hit(self,*args):
        return {'message':'Hand is ended.'}

    def stand(self,*args):
        return {'message':'Hand is ended.'}        

    def bet(self,*args):
        return {'message':'Betting is closed.'}

    def do(self):
        pass
        #print "resolving"

    def evaluate(self):
        return CleanStep

class CleanStep(games.GameStep):
    timeout = 1
    desc = "CleanStep"
    
    def evaluate(self):
        return ReadySeatsStep

    def do(self):
        #print "Clearing hands"
        self.table.clear()