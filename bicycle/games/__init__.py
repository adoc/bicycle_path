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


import itertools

from bicycle import map_serialize


try:
    range = xrange
except NameError:
    # Already Python 3 (hopefully) as `xrange` doesn't exist.
    pass


class InsufficientBankroll(Exception):
    """
    """
    pass



# These will be accessing the data model in other iterations of this func.
# Reason being is that player data state can be handled 
# outside the scope or the purpose of this module, but it must
# be accounted for properly to ensure the integrity and fidelity
# of the game.

def wager(player, amount):

    if player.bankroll >= amount:
        player.bankroll -= amount
        return amount

def collect(player, amount):

    player.bankroll += amount
    return amount



# Might move and rename.
# 
class Seats(list):
    """ Handles a list in a way more like static arrays. This works
    well when modeling position based entities like players, wagers, hands.

    This is surely wrong and should be fixed!
    """

    def __init__(self, n):
        if isinstance(n, int):
            list.__init__(self, [None for _ in range(n)])
        elif isinstance(n, list) or isinstance(n, tuple):
            list.__init__(self, n)

    def remove(self, item):
        """Looks for the `item` and if found will remove it and
        re-insert a `None`
        """
        i = list.index(self, item)
        list.pop(self, i)
        list.insert(self, i, None)

    def insert(self, i, item):
        """If `None` index is given, place item at first `None` valued
        index.
        If item at index `i` is not None, throw an error.
        Otherwise remove the `None` value and insert the item at the
        index.
        """
        if i is None:
            i = list.index(self, None)
        elif i < 0:
            raise IndexError("Must be a positive integer index.")
        elif self[i] is not None:
            self.insert(None, item)
            return
            #raise IndexError("Must insert in to a position with a `None` value.")

        list.pop(self, i)
        list.insert(self, i, item)

    # Do all or nothing. (extend, pop, etc.)
    #def append(self):
    #    raise IndexError("Cannot append to a `Seats` list.")


class Player(object):
    """
    """

    def __init__(self, seat_pref=None):
        self.bankroll = 0
        self.seat_pref = None

    def _gen_seralize(self, snoop=False):

        if self.seat_prof is not None:
            yield 'seat_pref', self.seat_pref


    def serialize(self, snoop=False):
        return dict(self._gen_seralize)

    def __json__(self):
        return self.serialize(snoop=False)


# We need to avoid the circular references.
# We need to account for back-end persistence.
class Table(object):
    """Handles players, seat positions, waiting to play list, bets??
    """

    def __init__(self, num_seats=6, to_play=[], to_leave=[], seats=None):
        """
        """

        self.num_seats = num_seats
        # Queue.
        self.to_play = to_play or []
        self.to_leave = to_leave or []
        self.seats = seats or Seats(self.num_seats)
        self.seat_prefs = {}

    def leave(self, player):
        """
        """

        if player in self.to_play:
            self.to_play.remove(player)
        elif player in self.seats:
            self.to_leave.append(player)
        else:
            raise ValueError("Given `player` is not seated or waiting.")

    def sit(self, player, index=None):
        """
        """

        assert index is None or index>=0, "`index` must be a positive integer."
        assert player not in self.seats
        assert player not in self.to_play

        self.seat_prefs[player] = index # Player's seat preference if any.
        self.to_play.append(player)

    def resolve(self):
        """
        """

        raise NotImplementedError()

    def cleanup(self):
        """
        This should occur last in the MRO from child classes.
        """

        # Remove players wanting to leave.
        for player in self.to_leave:
            self.seats.remove(player)

        def cleanup_to_play():
            if self.to_play and None in self.seats:
                player = self.to_play.pop(0)
                self.seats.insert(self.seat_prefs.get(player), player)
                cleanup_to_play()
        cleanup_to_play()

    def serialize(self, **kwa):
        """
        """

        return {'seats': map_serialize(self.seats, **kwa),
                'num_seats': self.num_seats}

    def __json__(self):
        return self.serialize(snoop=False)


class CardTable(Table):
    """
    """

    def __init__(self, hands=None, wagers=None, shoe=None, discard=None,
                 wager_func=wager, collect_func=collect, **kwa):
        # States that clear each game.
        self.hands = hands or Seats(self.num_seats)
        self.wagers = wagers or Seats(self.num_seats)

        # States that reset based on card threshold.
        self.shoe = shoe or Cards()
        self.discard = discard or Cards()

        self.wager_func = wager_func
        self.collect_func = collect_func

    def resolve(self):
        """
        """

        # Large percentage of card games should resolve with the top N
        # hands or at least hands in a sorted order.
        hands = sorted(self.hands,
                       key=lambda hand: int(hand))

        # List of winning hands only
        winning_hands = [hand for hand in hands if int(hand) == int(hands[0])]

        # Total pot.
        pot = sum([wager for wager in wagers if wager is not None])

        winnings = pot / len(winning_hands)

        




    def cleanup(self):
        """
        Be aware this clears all hands every game.
        """
        for player, hand, wager in zip(self.seats, self.hand, self.wagers):
            if hand is not None: # discard hands
                deal_all(hand, self.discard)

            if player is not None and wager is not None:
                self.collect_func(player, wager)

        Table.cleanup(self)


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





# this probable elsewhere

class Engine(object):
    """Machine all the states!
    """



