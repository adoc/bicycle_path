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


# This can possibly become part of the GameStep base.

class EngineStep(object):
    """
    """
    
    def __init__(self, step):
        """
        `step`  -   Instanced GameStep object.
        """

        self.step = step
        self.step.execute = self
        # self.result = None
        self.timer = threading.Timer(self.step.__timeout__ or ENGINE_TICK,
                                     self)
        self.started = time.time()
        self.timer.start()

    def __call__(self):
        """Essentially the "Next"
        """

        if self.timer is not None and not self.timer.finished:
            self.timer.cancel()
        self.result = self.step()
        return self.result

    @property
    def timeout(self):
        """
        """

        return math.floor(self.step.__timeout__ -
                          (time.time() - self.started))


class Engine(threading.Thread):
    """
    * Not sure how well this will play with Tornado IOLoop or
    asyncio (py 3.4)
    """

    def __init__(self, state):
        """
        """
        threading.Thread.__init__(self)
        assert isinstance(state, bicycle.game.GameState)

        self.state = state
        self.table = state.table

        self.__steps = self.game_steps = itertools.cycle(state.__game__)

        self.alive = False  # Engine thread alive.

    def __iter__(self):
        """
        """

        while self.alive is True:
            time.sleep(ENGINE_TICK)
            step = self.__steps.next()(self)    # Iterate to next step and
                                                # instance `GameStep.`
            while step.to_execute and self.alive is True:
                engine_step = EngineStep(step)
                yield step
                while not hasattr(engine_step, 'result') and self.alive is True:
                    time.sleep(ENGINE_TICK)
                if engine_step.result is True:
                    break

    def run(self):
        """
        """

        self.alive = True
        self.tick_count = 0

        handler = iter(self)

        while self.alive:
            self.game = handler.next()
            print(self.game)
            #time.sleep(ENGINE_TICK)

    def stop(self):
        """
        """
        
        self.alive = False
        self.timer.cancel()
        self.join()
        return True

# (c) 2011-2014 StudioCoda & Nicholas Long. All Rights Reserved