import itertools

import bicycle.table


def moretime(player):
    """The player has requested more time.
    """

    pass


def ready(player, state=None):
    """The player is ready. This is to provide a more intuitive
    UI response. Generally a bet will invoke a ready state, but
    there may be other indicators such as the player clicking on
    the table or interacting with the game.

    1. Player has indicated they want to play this game.

    2. Game in progress, player has indicated they want to play
    the next game.
    """

    if state is not None:
        # Set player ready state.
        pass

    # return player state.


def bet(self, player, amount):
    """Handle a bet.
    """

    # Set ready state for player on bet!
    self.ready(player, state=True)

    pass


class DealerEvents(object):
    """
    """

    pass


class GameStep(object):
    """
    GameStep instances should handle the various exceptions the lower
    order objects can raise.
    * GameStep instances never have a state that is used outside if its
    own context. I.e.; Don't serialize GameStep or assign instance
    vars that will be used outside of the GameStep instance.
    """

    def __init__(self, table):
        assert isinstance(table, bicycle.table.Table)
        self.table = table

    def __call__(self):
        raise NotImplementedError()


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

        # What checks do we run here? bankroll check?

        self.table.wager(player, amount)
        return True


class PrepareStep(SittableGameStepMixin, GameStep):
    """
    """

    __timeout__ = 1
    to_execute = True

    def __init__(self, *args, **kwa):
        GameStep.__init__(self, *args, **kwa)
        SittableGameStepMixin.__init__(self)

    def __call__(self): 
        """Prepare the table and return True if any seats are filled.
        """

        self.table.prepare()
        return any(self.table.seats)


class WagerStep(SittableGameStepMixin, WagerGameStepMixin, GameStep):
    """One or many players are wagering.
    """

    __timeout__ = 15
    to_execute = True  # Maybe base this instead on any(self.table.seats)

    def __init__(self, *args, **kwa):
        GameStep.__init__(self, *args, **kwa)
        WagerGameStepMixin.__init__(self)
        SittableGameStepMixin.__init__(self)

    def __call__(self):
        """Prepare the table and return True if any wagers are placed.
        """

        self.table.prepare()
        return any(self.table.wagers)


class DealStep(GameStep):
    """
    """

    __timeout__ = 0
    to_execute = True

    def __call__(self):
        self.table.deal_all()
        return True


class PlayerStep(GameStep):
    """One or many players are acting on the game state.
    """

    __timeout__ = 15
    to_execute = True

    def __call__(self):
        """
        """

        raise NotImplementedError()


class ResolveStep(GameStep):
    """Resolve the hands and wagers on the table.
    """

    __timeout__ = 10
    to_execute = True

    def __call__(self):
        """
        """
        self.table.resolve()
        return True # Not sure in what cases resolve would return False.


class CleanupStep(GameStep):
    """
    """

    __timeout__ = 0
    to_execute = True

    def __call__(self):
        self.table.cleanup()
        return True # Cleanup always returns True??


class GameState(object):
    """
    Passed to an engine. Game state and its `dict` and nested objects should
    hold the current state of a game.
    """

    __game__ = [] # Subclass to create the actual game.

    def __init__(self):
        """
        """

        self.step = itertools.cycle(self.__game__)

    # Serialization
    # =============
    def serialize(self, snoop=False):
        """Serialize the game step state for persistence or for
        communication.
        """

        pass

    def __json__(self):
        return self.serialize(snoop=False)