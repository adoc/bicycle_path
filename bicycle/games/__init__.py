"""Games base.
"""

# This should cover 99% of playing card games.


# Cleanup Step
#   Check deck state (reshuffle deck if needed)
# Bet Step
#   Take bets from players.
# Deal Step
#   Deal to active players.
# Resolve Step
#   Resolve Hands and Bets.


# These should both fire events and receive events.
# asyncio and other async compatibility should be considered but
#   let's see if we can avoid any hard dependencies.


class GameStepEvents(object):
    """
    """

    def sit(self, player):
        """Sit the player at the table.
        """

        pass

    def ready(self, player, state=None):
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

    def moretime(self, player):
        """The player has requested more time.
        """

        pass

    def bet(self, player, amount):
        """Handle a bet.
        """

        # Set ready state for player on bet!
        self.ready(player, state=True)

        pass

    def leave(self, player):
        """Player leaves the table.
        """

        pass


class GameStep(object):
    """
    """

    def serialize(self, snoop=False):
        """Serialize the game state for persistence or for
        communication.
        """

        pass

    def __json__(self):
        return self.serialize(snoop=False)


