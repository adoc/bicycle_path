"""
"""

import sys
import traceback
import json

import gevent

import socketio
import socketio.mixins
import socketio.namespace

import pyramid.httpexceptions
from pyramid.view import view_config


import bicycle.engine

from bicycle.game import (PrepareStep, WagerStep, PlayerStep,
                          ResolveStep, CleanupStep)
from bicycle.blackjack.game import InsuranceStep

from bicycle.player import Player
from bicycle.marshal import marshal_object


def _get_engine_player(request):
    try:
        engine_id = request.matchdict['engine']
        engine = request.registry.settings['engines'][engine_id]
        player = request.session['player']
    except KeyError:
        raise pyramid.httpexceptions.HTTPNotFound()
    else:
        return engine_id, engine, player


# Website Views
# =============
def meta_view(request):
    player = request.session['player'] = request.session.get('player', Player(bankroll=100000))
    return {'player': player}


def _dealer_observe(engine_id, engine, player):
    """
    """

    for k, v in marshal_object(engine.table.dealer).items():
        yield k, v

    yield 'hand', tuple(marshal_object(engine.table.dealer_hand))
    yield 'hand_total', int(engine.table.dealer_hand)


# Deprecating
def _player_list(engine_id, engine, player):
    """
    """

    for _player, hand, wager in zip(engine.table.seats, engine.table.hands,
                                    engine.table.wagers):

        def base_player():
            for k, v in marshal_object(_player, persist=_player is player).items():
                yield k, v

        if _player:
            this = dict(base_player())
            this['hand'] = marshal_object(hand, persist=_player is player)
            this['hand_total'] = int(hand)
            this['wager'] = wager.amount

            yield this
        else:
            yield None


def observe_seat(seat, player):
    """Observe a seat at a table.
    """
    for k, v in marshal_object(seat, persist=seat is player,
                               get_id=True).items():
        yield k, v


def seat_list(engine, player):
    """
    """
    for n, (seat, wager) in enumerate(zip(engine.table.seats,
                                          engine.table.wagers)):
        if seat:
            this = dict(observe_seat(seat, player))
            this['wager'] = wager.amount
            this['name'] = player.name

            yield this
        else:
            yield {'_id': -n - 1}   # This helps out
                                    # Backbone.Collection.set to
                                    # properly determine model
                                    # add/remove triggers.


def observe_hand(seat, hand, player):
    """
    """
    yield '_id', id(hand) # ??
    yield 'hand', marshal_object(hand, persist=seat is player)
    yield 'hand_total', int(hand)


def hand_list(engine, player):
    """
    """
    for n, (seat, hand) in enumerate(zip(engine.table.seats,
                                          engine.table.hands)):
        if seat:
            yield dict(observe_hand(seat, hand, player))
        else:
            yield {'_id': -n - 1}


'''
def _player_observe(engine_id, engine, player):
    """Observe the consuming player.
    """

    yield 'bankroll', player.bankroll

    if player in engine.table.seats:
        idx = engine.table.seats.index(player)
        hand = engine.table.hands[idx]
        wager = engine.table.wagers[idx]

        yield 'wager', wager.amount
        yield 'hand', marshal_object(hand, persist=True)
        yield 'hand_total', int(hand)
        yield 'in_seat', engine.table.seats.index(player)


def _engine_observe(engine_id, engine, player):
    """
    """

    yield 'step', engine.game.__class__.__name__
    yield 'dealer', dict(_dealer_observe(engine_id, engine, player))
    yield 'seats', list(_player_list(engine_id, engine, player))
    yield 'player', dict(_player_observe(engine_id, engine, player))

    yield 'accept_wager', isinstance(engine.game, (PrepareStep, WagerStep,
                                InsuranceStep, ResolveStep, CleanupStep))

    if isinstance(engine.game, PlayerStep):
        yield 'current_player', marshal_object(engine.game.player, persist=engine.game.player is player)
'''

# SocketIO Connectivity.
class RoomsMixin(socketio.mixins.RoomsMixin):
    def in_room(self, room):
        return self._get_room_name(room) in self.session['rooms']


def freeze(obj):
    """
    """
    def _freeze(obj):
        def do_list():
            for i in obj:
                yield _freeze(i)

        def do_dict():
            for k, v in obj.items():
                yield k, _freeze(v)

        if isinstance(obj, tuple):
            return tuple(do_list())

        elif isinstance(obj, list):
            return tuple(do_list())

        elif isinstance(obj, dict):
            return tuple(sorted(dict(do_dict()).items()))

        else:
            return obj

    return frozenset(_freeze(obj))


class EnabledNamespace(socketio.namespace.BaseNamespace, RoomsMixin):
    """Main Socketio Namespace parent class.
    """
    response_prefix = "response"

    def exception_handler_decorator(self, fn):
        """ Handle errors.
        """
        # Probably want to have a different exception handler in each
        # subclass.
        def wrap(*args, **kwargs):
            """Generic wrapper from 
            http://gevent-socketio.readthedocs.org/en/latest/namespace.html?highlight=error#socketio.namespace.BaseNamespace.recv_error
            """
            try:
                return fn(*args, **kwargs)
            except Exception, e:
                stack = traceback.format_exception(*sys.exc_info())
                print("socketio_exception",
                                 {"error": str(e),
                                  "trace": stack},
                                 self.request)
                # logging.getLogger('exc_logger').exception(e)
        return wrap

    def _event_data(self, data):
        """
        Returns (engine_id, engine)
        """
        engine_id = data['id']
        return engine_id, self.greenlets[engine_id]

    def initialize(self):
        """
        """
        self.engines = self.request.registry.settings['engines']
        self.greenlets = self.request.registry.settings['greenlets']
        self.player = meta_view(self.request)['player']

    def _watch(self, get_state, on_change, init_state_none=True):
        """Watch a given game state by calling `get_state`. When the
        state changes emit a 'change' event using the output of
        `on_change`.
        """
        _last_state = {} if init_state_none is True else get_state()
        while True:
            gevent.sleep(bicycle.engine.ENGINE_TICK)
            _current_state = get_state()
        
            _last_state_set = freeze(_last_state)
            _current_state_set = freeze(_current_state)

            if _last_state_set != _current_state_set:
                if not _last_state:
                    self.emit('reset', on_change())
                else:
                    self.emit('change', on_change())
                _last_state = _current_state

    def response(self, request_data, response_data):
        """
        """
        self.emit('_'.join([self.response_prefix, request_data['request_id']]),
                  response_data)

    def on_watch(self, data):
        """Simply watch/join an engine's stream.
        """
        def handle(*args):
            print("UH OHHHHHHH", args)

        id_, engine = self._event_data(data)
        if not self.in_room(id_): # Only if the socket is not already watching.
            self.join(id_)
            self.spawn(self.watch, id_, engine).link_exception(handle)
            self.response(data, True)
        else:
            self.response(data, False)


class EngineNamespace(EnabledNamespace):
    """
    """

    def on_list(self, data):
        """
        """

        self.response(data,
                      [engine for engine in
                            self.request.registry.settings['engines']])


class DealerNamespace(EnabledNamespace):
    """
    """
    
    def watch(self, engine_id, engine):
        """
        """

        def get_state():
            return dict(_dealer_observe(engine_id, engine, self.player))

        return self._watch(get_state, get_state, init_state_none=True)


class SeatsNamespace(EnabledNamespace):
    """
    """

    def watch(self, engine_id, engine):
        """
        """

        # def get_state():
        #     return tuple(_player_list(engine_id, engine, self.player))

        def get_state():
            return tuple(seat_list(engine, self.player))


        return self._watch(get_state, get_state, init_state_none=True)


class HandsNamespace(EnabledNamespace):
    """
    """

    def watch(self, engine_id, engine):
        """
        """

        def get_state():
            return tuple(hand_list(engine, self.player))

        return self._watch(get_state, get_state, init_state_none=True)


class TableStatusNamespace(EnabledNamespace):
    """
    """

    def watch(self, engine_id, engine):
        """
        """
        def get_state():
            """
            """
            return {'step': engine.game.__class__.__name__,
                    # Trigger at 1/2 timeout.
                    'timeout': engine.game.timeout <=
                                        engine.game.__timeout__ / 2}

        def show_state():
            return {'step': engine.game.__class__.__name__,
                    'timeout': engine.game.timeout}

        return self._watch(get_state, show_state, init_state_none=True)


class PlayerStatusNamespace(EnabledNamespace):
    """
    """

    def watch(self, engine_id, engine):
        """
        """

        def get_state():
            return {'bankroll': self.player.bankroll}

        return self._watch(get_state, get_state, init_state_none=True)


class TableControlsNamespace(EnabledNamespace):
    """
    """

    def watch(self, engine_id, engine):
        """
        """
        def get_state():
            return {
                'in_seat': engine.table.seats.index(self.player) if self.player in engine.table.seats else -1,
                'to_leave': self.player in engine.table.to_leave,
                'to_sit': self.player in engine.table.to_sit,
                'name': self.player.name if hasattr(self.player, 'name') else "Anon"
            }

        return self._watch(get_state, get_state, init_state_none=True)

    def on_sit(self, data):
        """
        """
        engine_id, engine = self._event_data(data)
        self.player.name = data.get('name')
        engine.game.sit(self.player)
        self.emit("response_"+data['request_id'], True)

    def on_leave(self, data):
        """
        """
        engine_id, engine = self._event_data(data)

        engine.game.leave(self.player)
        self.emit("response_"+data['request_id'], True)


class WagerControlsNamespace(EnabledNamespace):
    """
    """

    def watch(self, engine_id, engine):
        """
        """

        def get_state():
            if self.player in engine.table.seats:
                idx = engine.table.seats.index(self.player)
                wager = engine.table.wagers[idx]
                obj = marshal_object(wager, persist=True)
                obj['to_wager'] = engine.table.to_wager[self.player] if self.player in engine.table.to_wager else 0
                return obj
            else:
                return {}

        return self._watch(get_state, get_state, init_state_none=True)

    def on_wager(self, data):
        """
        """
        engine_id, engine = self._event_data(data)
        engine.game.wager(self.player, data['amount'])
        self.emit("response_"+data['request_id'], {'to_wager': engine.table.to_wager[self.player]})

    def on_clear(self, data):
        """
        """
        engine_id, engine = self._event_data(data)

        engine.game.clear_wager(self.player)
        self.response(data, {'to_wager': engine.table.to_wager[self.player]})


class GameControlsNamespace(EnabledNamespace):
    """Blackjack Game Controls.
    """

    def watch(self, engine_id, engine):
        """Watch the game controls. `show` 
        """

        def get_state():
            return {'show': hasattr(engine.game, 'player') and 
                            engine.game.player is self.player and
                            isinstance(engine.game, PlayerStep)}

        return self._watch(get_state, get_state, init_state_none=True)

    def on_hit(self, data):
        """Player "hits".
        """
        engine_id, engine = self._event_data(data)

        if (hasattr(engine.game, 'player') and
                self.player is engine.game.player): # If current player.
            engine.game.hit()
            self.response(data, True)
        else:
            self.response(data, False)

    def on_stand(self, data):
        """Player "stands".
        """
        engine_id, engine = self._event_data(data)
        if (hasattr(engine.game, 'player') and
                self.player is engine.game.player):
            engine.game.stand()
            self.response(data, True)
        else:
            self.response(data, False)

    def on_double(self, data):
        """Player "double downs".
        """
        engine_id, engine = self._event_data(data)
        if (hasattr(engine.game, 'player') and
                self.player is engine.game.player):
            engine.game.double()
            self.response(data, True)
        else:
            self.response(data, False)


@view_config(route_name='socket_endpoint', renderer='json')
def socket_endpoint(request):
    """Create a socket endpoint for the client.
    """

    return socketio.socketio_manage(request.environ, {
                                    '/engine': EngineNamespace,
                                    '/dealer': DealerNamespace,
                                    '/seats': SeatsNamespace,
                                    '/hands': HandsNamespace,
                                    '/player_status': PlayerStatusNamespace,
                                    '/table_status': TableStatusNamespace,
                                    '/table_controls': TableControlsNamespace,
                                    '/wager_controls': WagerControlsNamespace,
                                    '/game_controls': GameControlsNamespace
                                    }, request=request)