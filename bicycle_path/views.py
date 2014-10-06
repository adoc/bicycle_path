import json
import pyramid.httpexceptions
from pyramid.view import view_config

from bicycle.player import Player


def player_in_engines(request, player):
    def _player_in_engines():
        for key, engine in request.registry.settings['engines'].items():
            if player in engine.table.to_sit or player in engine.table.seats:
                yield key
    return list(_player_in_engines())


# Website Views
# =============
@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'bicycle_path'}


def game_view(request):
    player = request.session['player'] = request.session.get('player', Player(bankroll=100000))
    in_games = request.session.get('in_games',
                                   player_in_engines(request, player))
    return {'player': player,
            'in_games': json.dumps(in_games)}


# RESTful Views
# =============
# @view_config(route_name='engine_action', renderer='json')
def engine_action(request):
    engine = request.matchdict['engine']
    action = request.matchdict['action']

    return [engine, action]


@view_config(route_name='engine_sit', renderer='json')
def engine_sit(request):
    try:
        player = request.session['player']
        engine = request.registry.settings['engines'][request.matchdict['engine']]
    except KeyError:
        raise pyramid.httpexceptions.HTTPNotFound()
    else:
        return engine.game.sit(player)


@view_config(route_name='engine_leave', renderer='json')
def engine_leave(request):
    try:
        player = request.session['player']
        engine = request.registry.settings['engines'][request.matchdict['engine']]
    except KeyError:
        raise pyramid.httpexceptions.HTTPNotFound()
    else:
        return engine.game.leave(player)


@view_config(route_name='engine_list', renderer='json')
def engine_list(request):
    return [engine for engine in request.registry.settings['engines']]


@view_config(route_name='engine_observe', renderer='json')
def engine_observe(request):
    try:
        engine = request.registry.settings['engines'][request.matchdict['engine']]
    except KeyError:
        raise pyramid.httpexceptions.HTTPNotFound()
    else:
        query = engine.query()
        return query[0].__class__.__name__, query[1]