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


import inspect
import functools
import itertools

import bicycle.cards

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


# Should wagers be equivalent based on amount?
# 
@functools.total_ordering
class Wager(object):
    """Wager "spot" on a table.
    """
    def __init__(self, amount=0):
        self.amount = amount

    def __lt__(self, other):
        if isinstance(other, Wager):
            return self.amount < other.amount
        else:
            return self.amount < other

    def __eq__(self, other):
        if isinstance(other, Wager):
            return self.amount == other.amount
        else:
            return self.amount == other

    def __nonzero__(self):
        return self.amount > 0

    __bool__ = __nonzero__

    def __repr__(self):
        return "Wager(amount=%s) @ %s" % (self.amount, id(self))


class SplitWager(Wager):
    """A wager that may be split in to several parts.
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
#   Maybe `StaticList`
#
# Should this inherit from list?
#   What methods must be implemented for it to be list-like?
#       __iter__, __getitem__, ??
class Seats(list):
    """ Handles a list in a way more like static arrays. This works
    well when modeling position based entities like players, wagers, hands.

    This is surely wrong and should be fixed!
    """

    def __init__(self, n, base_obj_factory=lambda: None):
        self.base_obj_factory = base_obj_factory
        if isinstance(n, int):
            list.__init__(self, [self.base_obj_factory() for _ in range(n)])
        elif isinstance(n, list) or isinstance(n, tuple):
            list.__init__(self, n)

    @property
    def base_obj(self):
        return self.base_obj_factory()

    def remove(self, item):
        """Looks for the `item` and if found will remove it and
        re-insert a `base_obj`
        """
        i = list.index(self, item)
        list.pop(self, i)
        list.insert(self, i, self.base_obj)

    # This should be named `replace`
    def insert(self, i, item):
        """If `None` index is given, place item at first `None` valued
        index.
        If item at index `i` is not None, throw an error.
        Otherwise remove the `None` value and insert the item at the
        index.
        """
        if i is None:
            i = list.index(self, self.base_obj)
        elif i < 0:
            raise IndexError("Must be a positive integer index.")
        elif self[i] != self.base_obj:
            self.insert(None, item)
            return

        list.pop(self, i)
        list.insert(self, i, item)


class Player(object):
    """
    """

    def __init__(self, seat_pref=None, bankroll=0):
        self.bankroll = bankroll
        self.seat_pref = seat_pref

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
        if player in self.seat_prefs:
            del self.seat_prefs[player]

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
                if player in self.seat_prefs:
                    self.seats.insert(self.seat_prefs.pop(player), player)
                else:
                    self.seats.insert(None, player)
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
                 wager_func=wager, collect_func=collect, wager_cls=Wager,
                 **kwa):
        """
        """

        Table.__init__(self, **kwa)

        # States that clear each game.
        self.hands = hands or Seats(self.num_seats,
                                    base_obj_factory=bicycle.cards.Cards)
        self.wagers = wagers or Seats(self.num_seats,
                                      base_obj_factory=wager_cls)

        # States that reset based on card threshold.
        self.shoe = shoe or bicycle.cards.Cards()
        self.discard = discard or bicycle.cards.Cards()

        self.wager_func = wager_func
        self.collect_func = collect_func

        self.to_wager = {}

    # ===== Iterators
    def __iter__(self):
        """Basic iterator for the Table instance. Yields the `player`,
        `hand`, `wager` tuple.
        """
        for player, hand, wager in zip(self.seats, self.hands, self.wagers):
            yield player, hand, wager

    def _deal_all_iter(self):
        """Deal All iterator. Yields the `player`, `hand`, `wager`
        tuple for seated players. This is the most basic form of a
        deal only expecting that a player is in the seat.

        This method is overloaded in subclasses to add further deal
        caveats; e.g., games that require a wager before dealing to
        as seat.
        """

        for player, hand, wager in self:
            if player:
                yield player, hand, wager


    # -------- Player operations
    def leave(self, player, force=False):
        if player in self.to_wager:
            del self.to_wager[player]

        Table.leave(self, player)

    def wager(self, player, amount):
        self.to_wager[player] = self.to_wager.get(player, 0) + amount
        return amount

    # --------- Card shoe ops.
    # Most of these methods are candidates to be placed elsewhere.
    # Though I see no reason to put them in a dealer class.
    # Possibly the "game" class.
    def build(self, **kwa):
        bicycle.cards.build(self.shoe, **kwa)

    def pickup(self):
        """Pickup all the cards from the discard and deal them in to the shoe
        """

        bicycle.cards.deal_all(self.discard, self.shoe)

    # also might go elsewhere.
    def shuffle(self):
        bicycle.cards.shuffle(self.shoe)

    # Might go elsewhere. or be replaced.
    def deal_all(self):
        """
        """
        for _, hand, _ in self._deal_all_iter:
            bicycle.cards.deal(self.shoe, hand)

    # ------------ Table event methods.
    def last_chance(self):
        """
        """

        pass

    def resolve(self):
        """
        """
        # Not completed.

        # Large percentage of card games should resolve with the top N
        # hands or at least hands in a sorted order.
        hands = sorted(self.hands,
                       key=lambda hand: int(hand))

        # List of winning hands only
        winning_hands = [hand for hand in hands if int(hand) == int(hands[0])]

        # Total pot.
        pot = sum([wager for wager in wagers if wager is not None])

        winnings = pot / len(winning_hands)


    # Some of these operations need to be separated.
    #   Player seating and wager resolution. Though this hasn't caused
    #   any problems with the limited functional tests.
    def cleanup(self):
        """
        Be aware this clears all hands every game.
        """
        for player, hand, wager in self:
            if hand: # discard hands
                bicycle.cards.deal_all(hand, self.discard)

            if player and wager:
                self.collect_func(player, wager.amount)
                wager.amount = 0

        # Handle table seating.
        Table.cleanup(self)

        # Apply any queued bets.
        for player, _, wager in self:
            if player in self.to_wager:
                wager.amount = self.to_wager.pop(player)


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



