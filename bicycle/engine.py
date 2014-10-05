"""
"""

import time
import threading
import itertools

import bicycle.game
import bicycle.table


ENGINE_TICK = 0.1  # In seconds.


class Engine(threading.Thread):
    """
    * Not sure how well this will play with Tornado IOLoop or
    asyncio (py 3.4)
    """

    def __init__(self, state):
        """
        """
        assert isinstance(state, bicycle.game.GameState)
        threading.Thread.__init__(self)

        self.state = state
        self.table = state.table

        self.game_steps = itertools.cycle(state.__game__)

        self.game = None    # Current GameStep.
        self.timer = None   # Current GameStep timer.
        self.result = None  # Current GameStep result.

        self.alive = False  # Engine thread alive.
        self.tick_count = 0

    def execute_step(self):
        """This can be triggered by the timer or by a GameStep action.
        """
        self.timer.cancel() # Must cancel the time as a first action.
        self.result = self.game()
        if self.result is not True:
            self.set_timer()

    def set_timer(self):
        """This is the game step timer.
        """
        if self.timer is not None:
            self.timer.cancel()
        self.timer = threading.Timer(self.game.__timeout__, self.execute_step)
        self.timer.start()

    def handler(self):
        """
        """

        for game_step in self.game_steps:   # Iterate through the
                                            #   cycle of steps.
            self.result = None
            game = game_step(self)  # Instance the GameStep

            if game.to_execute is True:
                self.game = game
                self.set_timer()
                yield True

                while not self.result:
                    time.sleep(ENGINE_TICK)
                    self.tick_count += 1

            else:
                yield False

    def run(self):
        self.alive = True
        self.tick_count = 0

        handler = self.handler()

        while self.alive:
            handler.next()

            print("%s | %s" % (self.tick_count, self.game))
            print("Dealer Hand: %s" % self.table.dealer_hand)
            print("Table Hands: %s" % self.table.hands)

    def stop(self):
        self.alive = False


# (c) 2011-2014 StudioCoda & Nicholas Long. All Rights Reserved