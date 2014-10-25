"""
"""

import time
import threading
import itertools

import bicycle.game
import bicycle.table
import bicycle.marshal


ENGINE_TICK = 0.01   # In seconds.


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

    def __start_timer(self, timeout=None):
        #
        self.__timer = threading.Timer(timeout or self.step.__timeout__ or
                                       ENGINE_TICK, self)
        self.__timer.start()
        self.started = self.step._started = time.time()

    def delay(self, timeout=None):
        if timeout:
            timeout = self.step.timeout + timeout
        self.__timer.cancel()
        self.__start_timer(timeout)

    def cancel(self):
        """
        """

        if self.__timer is not None and not self.__timer.finished:
            self.__timer.cancel()


class Engine(object):
    """
    * Not sure how well this will play with Tornado IOLoop or
    asyncio (py 3.4)
    """

    def __init__(self, state, sleep_func=time.sleep):
        """
        """
        assert isinstance(state, bicycle.game.GameState)
        self.state = state
        self.table = state.table
        self.alive = False      # Engine thread alive.
        self.paused = False     # Engine thread paused.
        self.sleep = sleep_func

    def __iter__(self):
        """
        """

        steps = itertools.cycle(self.state.__game__)

        while self.alive is True:
            # print("outer engine")
            self.sleep(ENGINE_TICK)
            step = steps.next()(self)   # Iterate to next step and
                                        #   instance `GameStep.`

            while step.to_execute and self.alive is True:
                # print("middle engine")
                engine_step = EngineStep(step)

                # Running this in PlayerStep means this potentially can run
                # multiple times. This is part of the bad factoring in
                # PlayerStep and the Engine it self.
                hasattr(step, '__start__') and step.__start__()
                yield step, False

                # Wait for a result.
                while not hasattr(engine_step, 'result') and self.alive is True:
                    # print ("inner engine")
                    self.sleep(ENGINE_TICK)
                    while self.paused is True and self.alive is True:
                        engine_step.delay()
                        self.sleep(ENGINE_TICK)

                if engine_step.result is True:
                    yield step, True
                    break

                elif self.alive is not True:
                    engine_step.cancel()
                    break

        # print("ENGINE DONE")

    def run(self):
        """
        yields the game step and the steps finished state.
        """

        self.alive = True
        for finished, step in self:
            yield finished, step

    def kill(self):
        """
        """

        self.alive = False

    def pause(self):
        """
        """

        self.paused = True

    def unpause(self):
        """
        """

        self.paused = False


class EngineThread(threading.Thread):
    """
    """

    def __init__(self, engine):
        threading.Thread.__init__(self)
        self.engine = engine 

    def run(self):
        """Very simple execution example.
        """
        for finished, game in self.engine.run():
            self.finished, self.game = finished, game

    def kill(self):
        """
        """
        self.engine.kill()
        self.join()
        return True

    def pause(self):
        self.engine.pause()

    def unpause(self):
        self.engine.unpause()


try:
    import gevent
    import signal
except ImportError:
    pass
else:
    import gevent.monkey; gevent.monkey.patch_all()
    class EngineGreenlet(gevent.Greenlet):
        def __init__(self, engine):
            gevent.Greenlet.__init__(self)
            self.engine = engine
            self.engine.sleep = gevent.sleep
            self.table = self.engine.table

        def _run(self):
            """Very simple execution example.
            """
            for finished, game in self.engine.run():
                self.finished, self.game = finished, game

        def kill(self):
            """
            """
            self.engine.kill()
            gevent.kill(self)

        def pause(self):
            self.engine.pause()

        def unpause(self):
            self.engine.unpause()


# (c) 2011-2014 StudioCoda & Nicholas Long. All Rights Reserved