"""
"""

import math
import time
import threading
import itertools

import bicycle.game
import bicycle.table
import bicycle.marshal


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
        self.timer_started = time.time()
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
                    self.game.timeout = math.floor(self.game.__timeout__ -
                                            (time.time() - self.timer_started))
                    time.sleep(ENGINE_TICK)

            else:
                yield False

    def query(self):
        """Query the engine for game state.
        """

        return self.game, bicycle.marshal.marshal_object(self.game)

    def run(self):
        self.alive = True
        self.tick_count = 0

        handler = self.handler()

        while self.alive:
            handler.next()

    def stop(self):
        self.alive = False


# (c) 2011-2014 StudioCoda & Nicholas Long. All Rights Reserved