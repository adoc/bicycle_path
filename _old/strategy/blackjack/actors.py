from . import DealerStrategy, PlayerStrategy
from threading import Timer

class Actor(object):
    """ Timer/actor for dealer. """
    timeout = 1
    def start(self):
        self.timer = Timer(self.timeout,self.act)
        self.timer.start()    

class PlayerActor(Actor): 
    """ """
    strategy = PlayerStrategy()

    def __init__(self,seat,dealershow,hitfunc,standfunc,doublehitfunc,doublestandfunc,splitfunc):
        self.seat = seat
        self.dealershow = dealershow
        self.hit = hitfunc
        self.stand = standfunc
        self.doublehit = doublehitfunc
        self.doublestand = doublestandfunc
        self.split = splitfunc

        #self.act()

    def act(self):
        action = self.strategy.advise(self.seat.hand,self.dealershow)
        if action=="S":
            self.stand(self.seat.player)
        elif action=="H":
            self.hit(self.seat.player)
        elif action=="Hd":
            self.doublehit(self.seat.player)
        elif action=="Hu":
            self.hit(self.seat.player)
        elif action=="P":
            self.split(self.seat.player)
        elif action=="Sd":
            self.doublestand(self.seat.player)

        self.start()


class DealerActor(Actor):
    """ """
    strategy = DealerStrategy()    
    def __init__(self,seat,hitfunc,standfunc):
        self.seat = seat
        self.hit = hitfunc
        self.stand = standfunc
        self.act()

    def act(self):
        action = self.strategy.advise(self.seat.hand)
        if action:
            self.hit(self.seat.player)
        else:
            self.stand(self.seat.player)

        self.start()