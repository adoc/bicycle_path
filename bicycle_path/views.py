import json

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
@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'bicycle_path'}


## OUT!
def meta_view(request):
    player = request.session['player'] = request.session.get('player', Player(bankroll=100000))
    return {'player': player}


# RESTful Views
# =============
@view_config(route_name='engine_list', renderer='json')
def engine_list(request):
    print ("GET ENGIEN LIST!!!!")
    return [engine for engine in request.registry.settings['engines']]


@view_config(route_name='engine_wager', renderer='json')
def engine_wager(request):
    _, engine, player = _get_engine_player(request)
    try:
        amount = int(request.params['amount'])
    except (KeyError, ValueError, TypeError):
        raise pyramid.httpexceptions.HTTPBadRequest()
    else:
        engine.game.wager(player, amount)
        return True
# ----

# Blackjack Game Controls.
@view_config(route_name='engine_hit', renderer='json')
def engine_hit(request):
    _, engine, player = _get_engine_player(request)
    if (hasattr(engine.game, 'player') and
            player is engine.game.player): # If current player.
        engine.game.hit()
        return True


@view_config(route_name='engine_stand', renderer='json')
def engine_stand(request):
    _, engine, player = _get_engine_player(request)
    if player is engine.game.player:
        engine.game.stand()
        return True


@view_config(route_name='engine_double', renderer='json')
def engine_double(request):
    _, engine, player = _get_engine_player(request)
    if player is engine.game.player:
        engine.game.double()
        return True


@view_config(route_name='engine_start', renderer='json')
def engine_start(request):
    _, engine, _ = _get_engine_player(request)
    engine.unpause()
    return True


@view_config(route_name='engine_pause', renderer='json')
def engine_pause(request):
    _, engine, _ = _get_engine_player(request)
    engine.pause()
    return True
# ----


# deprecated. here for reference.
def __out_engine_observe(engine_id, engine, player):
    """
    """

    # Combine the marshaled game state.
    for k, v in marshal_object(engine.game).items():
        yield k, v

    yield 'engine_id', engine_id
    yield 'step', engine.game.__class__.__name__
    yield 'in_game', (player in engine.table.to_sit or
                        player in engine.table.seats and
                        player not in engine.table.to_leave)

    yield 'player_bankroll', player.bankroll

    def sum_cards(hand):
        # Broken handling does not account for aces.
        # We need a sum in the Hand class that doesn't total
        # face down cards.
        for card in hand:
            if card.up is True:
                yield int(card)

    yield 'dealer_total', int(engine.table.dealer_hand)
    yield 'shown_totals', [int(hand)
                                if hand else 0 for hand in engine.table.hands]

    if player in engine.table.seats:
        idx = engine.table.seats.index(player)
        hand = engine.table.seats[idx]

        # Some of these can be incorporated in to the table state.
        yield 'your_turn', (hasattr(engine.game, 'player') and
                            engine.game.player is player)

        yield 'in_seat', (player in engine.table.seats and idx)

        yield 'your_hand', marshal_object(hand, persist=True)
        yield 'hand_total', int(hand)


@view_config(route_name='engine_poll', renderer='json')
def engine_poll(request):
    """
    """

    return dict(_engine_observe(*_get_engine_player(request)))


# Backbone Models - Player
@view_config(route_name='player_observe', renderer='json')
def player_observe(request):
    """
    """

    return dict(_player_observe(*_get_engine_player(request)))


def _dealer_observe(engine_id, engine, player):
    """
    """

    for k, v in marshal_object(engine.table.dealer).items():
        yield k, v

    yield 'hand', marshal_object(engine.table.dealer_hand)
    yield 'hand_total', int(engine.table.dealer_hand)


def _player_list(engine_id, engine, player):
    """
    """

    for _player, hand, wager in zip(engine.table.seats, engine.table.hands,
                                    engine.table.wagers):

        def base_player():
            #if _player:
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


import gevent
from pprint import pprint


# SocketIO Connectivity.
class RoomsMixin(socketio.mixins.RoomsMixin):
    def in_room(self, room):
        return self._get_room_name(room) in self.session['rooms']


class EnabledNamespace(socketio.namespace.BaseNamespace, RoomsMixin):
    """
    """
    response_prefix = "response"

    def _event_data(self, data):
        """
        Returns (engine_id, engine)
        """
        engine_id = data['id']
        return engine_id, self.greenlets[engine_id]

    def initialize(self):
        self.engines = self.request.registry.settings['engines']
        self.greenlets = self.request.registry.settings['greenlets']
        self.player = meta_view(self.request)['player']

    def _watch(self, get_state, on_change, init_state_none=True):

        _last_state = {} if init_state_none is True else get_state()
        while True:
            gevent.sleep(bicycle.engine.ENGINE_TICK)
            _current_state = get_state()
            
            _last_state_set = frozenset(_last_state.items())
            _current_state_set = frozenset(_current_state.items())

            if _last_state_set != _current_state_set:
                _last_state = _current_state
                self.emit('change',
                            on_change())

    def response(self, request_data, response_data):
        self.emit('_'.join([self.response_prefix, request_data['request_id']]),
                  response_data)

    def on_watch(self, data):
        """Simply watch/join an engine's stream.
        """
        def handle():
            print("uh ohhhh")

        # TODO: Might deprecate `pulse_on_join`
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

    def watch(self, engine_id, engine):
        """
        """

        # TODO: Should be reduced to the step. The rest of the game
        #   state is exposed through other socket namespaces.

        return self._watch(
                lambda: {'step': engine.game},
                lambda: dict(_engine_observe(engine_id, engine, self.player)),
                init_state_none=True)

    def on_list(self, data):
        """
        """

        self.response(data,
                      [engine for engine in
                            self.request.registry.settings['engines']])

    def on_read(self, data):
        """
        """
        engine_id, engine = self._event_data(data)

        if data['ns'] == "game":
            response_data = dict(_engine_observe(engine_id, engine,
                                                 self.player))

        self.response(data, response_data);


class DealerNamespace(EnabledNamespace):
    """
    """
    pass

class SeatNamespace(EnabledNamespace):
    """
    """

    def watch(self, engine_id, engine):
        """
        """

        return self._watch(
                # lambda: hash(frozenset(self.player.__dict__.items())),
                lambda: self.player.__dict__,
                lambda: dict(_player_observe(engine_id, engine, player)),
                init_state_none=True)


class PlayerStatusNamespace(EnabledNamespace):
    
    def watch(self, engine_id, engine):
        """
        """

        def get_state():
            return {'bankroll': self.player.bankroll}

        return self._watch(get_state, get_state ,init_state_none=True)


class TableControlsNamespace(EnabledNamespace):
    """
    """
    def watch(self, engine_id, engine):
        """
        """
        def get_state():
            return {
                'in_seat': engine.table.seats.index(self.player) if self.player in engine.table.seats else -1,
                'to_leave': self.player in engine.table.to_leave
            }

        return self._watch(get_state, get_state, init_state_none=True)

    def on_sit(self, data):
        """
        """
        engine_id, engine = self._event_data(data)

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


@view_config(route_name='socket_endpoint', renderer='json')
def socket_endpoint(request):
    """Create a socket endpoint for the client.
    """

    return socketio.socketio_manage(request.environ, {
                                    '/engine': EngineNamespace,
                                    '/dealer': DealerNamespace,
                                    '/seat': SeatNamespace,
                                    '/player_status': PlayerStatusNamespace,
                                    '/table_controls': TableControlsNamespace,
                                    '/wager_controls': WagerControlsNamespace
                                    }, request=request)