import json
import pyramid.httpexceptions
from pyramid.view import view_config

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


def meta_view(request):
    player = request.session['player'] = request.session.get('player', Player(bankroll=100000))

    return {'player': player}


# RESTful Views
# =============
@view_config(route_name='engine_list', renderer='json')
def engine_list(request):
    return [engine for engine in request.registry.settings['engines']]


@view_config(route_name='engine_sit', renderer='json')
def engine_sit(request):
    _, engine, player = _get_engine_player(request)
    return engine.game.sit(player)


@view_config(route_name='engine_leave', renderer='json')
def engine_leave(request):
    _, engine, player = _get_engine_player(request)
    return engine.game.leave(player)


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


@view_config(route_name='engine_hit', renderer='json')
def engine_hit(request):
    _, engine, player = _get_engine_player(request)
    if player is engine.game.player: # If current player.
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


@view_config(route_name='engine_pause', renderer='json')
def engine_pause(request):
    _, engine, player = _get_engine_player(request)
    engine.pause()


def _engine_observation(engine_id, engine, player):
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

    yield 'dealer_total', int(engine.table.dealer_hand) #  sum(sum_cards(engine.table.dealer_hand))
    yield 'shown_totals', [int(hand) if hand else 0 for hand in engine.table.hands] # [sum(sum_cards(hand)) if hand else 0 for hand in engine.table.hands]

    if player in engine.table.seats:
        idx = engine.table.seats.index(player)
        hand = engine.table.hands[idx]

        # Some of these can be incorporated in to the table state.
        yield 'your_turn', (hasattr(engine.game, 'player') and
                            engine.game.player is player)

        yield 'in_seat', (player in engine.table.seats and
                            engine.table.seats.index(player))

        yield 'your_hand', marshal_object(hand, persist=True)
        yield 'hand_total', int(hand)


@view_config(route_name='engine_observe', renderer='json')
def engine_observe(request):
    return dict(_engine_observation(*_get_engine_player(request)))