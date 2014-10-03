"""
"""

import threading
import time
import bicycle.game
import bicycle.table


class SimpleEngine(object):
    """
    """

    def __init__(self, game_state, table):
        assert isinstance(game_state, bicycle.game.GameState)
        assert isinstance(table, bicycle.table.Table)
        self._game_state = game_state
        self._table = table
        self.step =None

    def execute(self):
        """
        """

        for game_step in self._game_state.step:

            self.step = game_step(self._table) # Instance the GameStep
            
            while True:
                # This is all wonky. Fix it!
                if self.step.to_execute is True:
                    time.sleep(self.step.__timeout__)
                    result = self.step() # Execute the step.
                    yield self.step, result

                    if result is True:
                        break

                else:
                    break


class EngineThread(threading.Thread):
    """
    """

    def __init__(self, engine):
        threading.Thread.__init__(self)
        self.engine = engine
        self.alive = False

    def run(self):
        self.alive = True
        e = self.engine.execute()

        while self.alive:
            print(e.next())

    def kill(self):
        self.alive = False

