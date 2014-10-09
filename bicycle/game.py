"""
"""

import math
import time
import bicycle.table
import bicycle.engine


class SittableGameStepMixin(object):
    """Allows players to be seated or queued to sit at the table.
    """

    # Actions API
    # ===========
    def sit(self, player, index=None):
        """Queue up the player to be seated at the table.
        """
        if self.table.can_sit(player) is True:
            self.table.sit(player, index=index)
            return True

    def leave(self, player):
        """Queue up the player to leave the table.
        """
        if self.table.can_leave(player) is True:
            self.table.leave(player)
            return True


class WagerGameStepMixin(object):
    """Game Step Mixin to allow for wagering at the table.
    """

    def wager(self, player, amount):
        """
        """
        self.delay(1)

        # What checks do we run here? bankroll check?

        self.table.wager(player, amount)
        return True


class GameStep(object):
    """
    * GameStep instances never have a state that is used outside if its
    own context. I.e.; Don't serialize GameStep or assign instance
    vars that will be used outside of the GameStep instance.
    """
    # GameStep instances should handle the various exceptions the lower
    #   order objects can raise.

    __timeout__ = 0
    __persistent_keys__ = ['table']
    __view_keys__ = ['table', 'timeout']

    to_execute = True

    def __init__(self, engine):
        """
        """

        assert isinstance(engine, bicycle.engine.Engine)
        self.engine = engine
        self.table = engine.table
        self.state = engine.state

    @property
    def timeout(self):
        """
        """

        return math.floor(self.__timeout__ -
                          (time.time() - self._started))

    def __call__(self):
        """
        """

        raise NotImplementedError()


class PrepareStep(SittableGameStepMixin, GameStep):
    """
    """

    def __init__(self, engine):
        """
        """

        GameStep.__init__(self, engine)
        SittableGameStepMixin.__init__(self)

    def __call__(self): 
        """Prepare the table and return True if any seats are filled.
        """

        self.table.prepare()
        return any(self.table.seats)


class WagerStep(SittableGameStepMixin, WagerGameStepMixin, GameStep):
    """One or many players are wagering.
    """

    __timeout__ = 5

    def __init__(self, engine):
        """
        """

        GameStep.__init__(self, engine)
        WagerGameStepMixin.__init__(self)
        SittableGameStepMixin.__init__(self)

    def __call__(self):
        """Prepare the table and return True if any wagers are placed.
        """

        self.table.prepare()
        return any(self.table.wagers)

        # What is this cleaning up??
        # result = any(self.table.wagers)
        # if result is False:
        #     self.table.cleanup()
        # return result


class DealStep(GameStep):
    """
    """

    def __call__(self):
        self.table.deal_all()
        return True


class PlayerStep(GameStep):
    """One or many players are acting on the game state. Iterate
    through the players.
    """

    __timeout__ = 15

    def __init__(self, engine):
        """
        """

        GameStep.__init__(self, engine)
        self._play_all = self.table._play_all_iter() # Set up iterator.

    def __start__(self):
        next = self.next() # Get first player.
        assert next is True     # Assert on second line in case code is
                                # optimized to .pyo

    def next(self):
        """
        """

        try:
            self._play_item = self._play_all.next()
            return True
        except StopIteration:
            return False

    def __call__(self):
        """
        """

        return not self.next()


class ResolveStep(GameStep):
    """Resolve the hands and wagers on the table.
    """

    __timeout__ = 10

    def __call__(self):
        """
        """

        self.table.resolve()
        return True # Not sure in what cases resolve would return False.


class CleanupStep(GameStep):
    """
    """

    def __call__(self):
        """
        """

        self.table.cleanup()
        return True # Cleanup always returns True??


# Possibly refactor The GameStep iterations to be part of the
#   GameState.
class GameState(object):
    """
    Passed to an engine. Game state and its `dict` and nested objects should
    hold the current state of a game.
    """

    __game__ = []       # Subclass to create the actual game.
    __table__ = bicycle.table.Table

    def __init__(self, *args, **kwa):
        """Return the `GameState` with instanced `Table`.
        """

        self.table = self.__table__(*args, **kwa)   # Instance a table.


# (c) 2011-2014 StudioCoda & Nicholas Long. All Rights Reserved