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


# These should both fire events and receive events??
# asyncio and other async compatibility should be considered but
#   let's see if we can avoid any hard dependencies.


import inspect
import functools
import itertools

import bicycle.card

from bicycle import random, map_serialize


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
    """
    """

    if player.bankroll >= amount:
        player.bankroll -= amount
        return amount

def collect(player, amount):
    """
    """

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

    def increment(self):
        raise NotImplementedError()

    @property
    def base_obj(self):
        return self.base_obj_factory()

    def remove(self, item):
        """Looks for the `item` and if found will remove it and
        re-insert a `base_obj`
        """
        i = list.index(self, item)
        self.pop(i)

    def pop(self, i):
        """
        """
        list.pop(self, i)
        list.insert(self, i, self.base_obj)

    # Should this be named `replace`??
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


class RotatingDealer(Seats):
    """Used in place of `Seats` in the cases of a rotating deal.
    """
    def __init__(self, n, offset=0, **kwa):
        Seats.__init__(self, n, **kwa)
        self._offset = 0

    def __iter__(self):
        """
        Used to facilitate position based dealing, betting, etc.
        """
        cycle_self = itertools.cycle(list.__iter__(self))
        self._offset = self._offset % len(self)
        for i in range(self._offset):
            cycle_self.next()

        for _ in list.__iter__(self):
            yield cycle_self.next()

    def increment(self):
        self._offset += 1

    def rotate(self):
        self.increment()


class RandomDealer(RotatingDealer):
    """Chooses a random dealer on `increment`.
    """

    def rotate(self):
        """
        """
        self._offset = self.index(random.choice(self))


class Table(object):
    """Handles players, seat positions, waiting to play list, bets??
    """

    # For (de)marshaling.
    __persistent_keys__ = ['to_play', 'to_leave', 'seats', 'seat_prefs']
    __view_keys__ = ['to_play', 'seats']

    def __init__(self, num_seats=6, seats_cls=Seats):
        """
        params
        ------
        num_seats   (int)   Number of seats available at this table.
        to_play     (list)  List of Players waiting to play at this
                            table.
        seat_prefs  (dict)  Player instance as key to integer seat
                            position preference.
        seats_cls   (Seats) Pass `RotatingDealer` or other `Seats`
                            subclasses. Implement

        iterators
        ---------
        __iter__

        actions/events
        --------------
        rotate_deal
        leave
        sit
        resolve
        _handle_seating
        cleanup

        serialization
        -------------
        serialize
        __json__
        """

        # Queues.
        self.to_play = []
        self.to_leave = []

        # Position states.
        self.seats = seats_cls(num_seats)

        # Object metadata.
        self.seat_prefs = {}

    # Iterators
    # =========
    def __iter__(self):
        """
        """
        for seat in self.seats:
            yield seat

    # Misc
    def can_sit(self, player):
        """Return True if the player may sit at this table or be queued
        to sit.
        """
        return (player not in self.seats and
                player not in self.to_play)

    def can_leave(self, player):
        """Return True if the player may leave this table or be queued
        to leave it.
        """
        return player not in self.to_leave and (player in self.seats or
                                                player in self.to_play)

    # Actions/Events
    # ==============
    def sit(self, player, index=None):
        """
        """

        assert index is None or index >= 0, ("`index` must be a positive "
                                             "integer.")
        assert player not in self.seats 
        assert player not in self.to_play
        # If a game table requires that a player may play multiple
        #   seats, this should be implemented in the higher layers of
        #   the architecture. i.e.; multiple Player instances assigned
        #   to one player data model/view/etc.

        if index is not None:
            self.seat_prefs[player] = index  # Player's seat preference
                                             # if any.
        self.to_play.append(player)

    def leave(self, player):
        """Queue the player to leave this table.
        """

        assert player not in self.to_leave
        assert player in self.seats or player in self.to_play

        # Remove from seat position preferences.
        if player in self.seat_prefs:
            del self.seat_prefs[player]

        # Remove from `to_play` queue.
        if player in self.to_play:
            self.to_play.remove(player)

        # Put in `to_leave` queue.
        if player in self.seats:
            self.to_leave.append(player)

    def rotate_deal(self):
        """
        """
        self.seats.increment()

    def resolve(self):
        """Resolve the hands.
        """

        raise NotImplementedError()

    def prepare(self):
        """Seat the waiting players in the `to_play` queue.
        """
        def seat_to_play():
            if self.to_play and None in self.seats:
                player = self.to_play.pop(0)
                if player in self.seat_prefs:
                    self.seats.insert(self.seat_prefs.pop(player), player)
                else:
                    self.seats.insert(None, player)
                seat_to_play()
        seat_to_play()

    def cleanup(self):
        """Unseats players in the `to_leave` queue.
        """

        for player in self.to_leave:
            self.seats.remove(player)

    # Removing in lieu of __presistant_keys && __views_keys
    def serialize(self, **kwa):
        """
        """

        return {'seats': map_serialize(self.seats, **kwa),
                'num_seats': self.num_seats}

    # Removing in lieu of __presistant_keys && __views_keys
    def __json__(self):
        return self.serialize(snoop=False)


class CardTable(Table):
    """
    """

    def __init__(self, num_seats=6, reshuffle_threshold=1.0,
                 card_cls=bicycle.card.Card, hand_cls=bicycle.card.Cards,
                 seats_cls=Seats, **kwa):
        """
        """

        Table.__init__(self, num_seats=num_seats, seats_cls=seats_cls, **kwa)

        # "hands" should be meta as well as wagers to facilitate
        #   multiple hand. Like in the case of a blackjack split.
        self.hands = seats_cls(num_seats,
                               base_obj_factory=hand_cls)

        self.shoe = bicycle.card.Cards()        # Dealing shoe
        self.discard = bicycle.card.Cards()     # Discard pile
        self.reshuffle_threshold = reshuffle_threshold

        self.card_cls = card_cls

    @classmethod
    def subtable(cls, table):
        # Idea for subtable, but is full of problems.
        subtable = cls(len(table.seats), seats_cls=table.seats.__class__)

        subtable.to_play = table.to_play
        subtable.to_leave = table.to_leave
        subtable.seats = table.seats
        subtable.seat_prefs = table.seat_prefs

    # Iterators
    # =========
    def __iter__(self):
        """Basic iterator for the Table instance. Yields the `player`,
        `hand`, `wager` tuple.
        """
        for seat, hand in zip(self.seats, self.hands):
            yield seat, hand

    def _deal_all_iter(self):
        """Deal All iterator. Yields the `player`, `hand`, `wager`
        tuple for seated players. This is the most basic form of a
        deal only expecting that a player is in the seat.

        This method is overloaded in subclasses to add further deal
        caveats; e.g., games that require a wager before dealing to
        as seat.
        """

        for player, hand in self:
            if player:
                yield hand, None

    def players(self):
        """
        """

        pass

    # Card/Shoe Actions
    # -----------------
    # Most of these methods are candidates to be placed elsewhere.
    # Though I see no reason to put them in a dealer class.
    # Possibly the "game" class.
    def build(self, **kwa):
        """
        """
        self.shoe.build(card_cls=self.card_cls, **kwa)

    def shuffle(self):
        self.shoe.shuffle()

    def pickup(self):
        """Pickup all the cards from the discard and deal them in to the shoe
        """

        self.discard.discard(self.shoe)

    def deal_all(self):
        """
        """
        # _deal_all_iter can return (player, hand) or (player, hand, wager)
        #   depending on the class implementation.
        for hand, opts in self._deal_all_iter():
            self.deal(hand, **(opts or {}))

    def deal(self, hand, **opts):
        self.shoe.deal(hand, **opts)

    def rotate_deal(self):
        """
        """

        self.hands.increment()
        Table.rotate_deal(self)

    # Table Events
    # ------------
    def resolve(self):
        """Resolve the hands.
        """

        # Large percentage of card games should resolve with the top N
        # hands or at least hands in a sorted order.
        return sorted(self.hands,
                      key=lambda hand: int(hand))

    def prepare(self):
        """Check the shoe.
        """

        Table.prepare(self)

        if len(self.shoe) + len(self.discard) == 0:
            self.build()

        if self.shoe.diff_check(self.reshuffle_threshold) is True:
            self.pickup()

        self.shuffle()  # Let's just shuffle every time. This should
                        #   add a little extra entropy since the number
                        #   of prepare calls is essentially random and
                        #   based on player interaction.

    def cleanup(self):
        """Discard all players hands.
        """

        for player, hand in CardTable.__iter__(self):
            if hand:
                hand.discard(self.discard)

        Table.cleanup(self)


# Possibly a wrapped instance than a mixin should allow for side bets.
class WagerTableMixin(object):
    """
    """

    def __init__(self, num_seats=6, wager_cls=Wager, wager_func=wager,
                 collect_wager_func=collect, seats_cls=Seats, **kwa):

        self.wagers = seats_cls(num_seats,
                                      base_obj_factory=wager_cls)

        self.wager_func = wager_func
        self.collect_wager_func = collect_wager_func
        self.to_wager = {}

    # Iterators
    # =========
    def __iter__(self):
        for seat, wager in zip(self.seats, self.wagers):
            yield seat, wager

    # Player Actions
    # --------------
    def leave(self, player):
        """Queue up a Player exit from the table.
        """

        if player in self.to_wager:
            del self.to_wager[player]

        super(WagerTableMixin, self).leave(player)

    def wager(self, player, amount):
        """Queue up a wager.
        """
        self.to_wager[player] = self.to_wager.get(player, 0) + amount
        return amount

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

    def prepare(self):
        """
        """

        super(WagerTableMixin, self).prepare()

        for player, wager in WagerTableMixin.__iter__(self):
            if player in self.to_wager:
                wager.amount = self.to_wager.pop(player)

    def cleanup(self):
        """
        """

        for player, wager in WagerTableMixin.__iter__(self):
            if player and wager:
                self.collect_wager_func(player, wager.amount)
                wager.amount = 0

        super(WagerTableMixin, self).cleanup()