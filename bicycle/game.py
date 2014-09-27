

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
    """

    def __init__(self):
        self.step_index = None


    def trigger(self, event):
        """
        """

        pass

    def serialize(self, snoop=False):
        """Serialize the game step state for persistence or for
        communication.
        """

        pass

    def __json__(self):
        return self.serialize(snoop=False)


class CleanupStep(GameStep):
    """
    """

    timeout = 0


class BetStep(GameStep):
    """
    """

    timeout = 10


class DealStep(GameStep):
    """
    """

    timeout = 0


class ResolveStep(GameStep):
    """
    """

    timeout = 10


# Just the default "game", mainly for testing and demonstration
#   purposes.
game_steps = [CleanupStep, BetStep, DealStep, ResolveStep]



# This is also probably going elsewhere


class GameState(object):
    """
    Passed to an engine. Game state and its `dict` and nested objects should
    hold the current state of a game.
    """

    def __init__(self, table, step, game_steps=game_steps):
        """
        """

        self.table = table
        self._current_step = step
        self.game_steps = itertools.cycle(game_steps)


    def do(self):
        """
        """


    def advance(self):
        """
        """


class Engine(object):
    """Machine all the states!
    """

    pass