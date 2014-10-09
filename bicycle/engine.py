"""
"""

import time
import threading
import itertools

import bicycle.game
import bicycle.table
import bicycle.marshal


ENGINE_TICK = 0.1   # In seconds.


class EngineStep(object):
    """
    """
    
    def __init__(self, step):
        """
        `step`  -   Instanced GameStep object.
        """

        self.step = step
        self.step.execute = self # Set callback on the step.
                                 # This indicates there is a better factor.
        self.step.delay = self.delay
        self.__start_timer()

    def __call__(self):
        """Cancel the timer and store the result from the `GameStep`.
        """
        self.cancel()
        self.result = self.step()
        return self.result

    def __start_timer(self):
        #
        self.__timer = threading.Timer(self.step.__timeout__ or ENGINE_TICK,
                                       self)
        self.__timer.start()
        self.step._started = time.time()

    delay = __start_timer

    def cancel(self):
        """
        """

        if self.__timer is not None and not self.__timer.finished:
            self.__timer.cancel()


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
        self.alive = False  # Engine thread alive.
        self.paused = False

    def __iter__(self):
        """
        """

        steps = itertools.cycle(self.state.__game__)

        while self.alive is True:
            time.sleep(ENGINE_TICK)
            step = steps.next()(self)   # Iterate to next step and
                                        #   instance `GameStep.`
            hasattr(step, '__start__') and step.__start__()
            while step.to_execute and self.alive is True:
                engine_step = EngineStep(step)
                yield step
                
                # Wait for a result.
                while not hasattr(engine_step, 'result') and self.alive is True:
                    time.sleep(ENGINE_TICK)
                    while self.paused is True:
                        engine_step.delay()
                        time.sleep(ENGINE_TICK)

                if engine_step.result is True:
                    break
                elif self.alive is not True:
                    engine_step.cancel()
                    break

    def run(self):
        """Very simple execution example.
        """

        self.alive = True
        handler = iter(self)
        while self.alive:
            self.game = handler.next()
            # print(self.game)  # This will ultimately be a message
                                #   out to the appropriate websocket.

    def stop(self):
        """
        """

        self.alive = False
        # self.timer.cancel()
        self.join()
        return True

    def pause(self):
        self.paused = not self.paused


# (c) 2011-2014 StudioCoda & Nicholas Long. All Rights Reserved