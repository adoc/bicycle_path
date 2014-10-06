import atexit
from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    
    config.include('pyramid_mako')
    config.include('pyramid_chameleon')
    config.include('pyramid_beaker')

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('game', '/game')
    
    config.add_view('bicycle_path.views.game_view', route_name='game',
                    renderer='templates/game.html.mako')

    # REST Routes
    config.add_route('engine_list', '/api/v1/engines')
    config.add_route('engine_observe', '/api/v1/engines/{engine}/observe')
    config.add_route('engine_sit', '/api/v1/engines/{engine}/sit')
    config.add_route('engine_leave', '/api/v1/engines/{engine}/leave')
    config.add_route('engine_player', '/api/v1/game')

    config.add_view('bicycle_path.views.game_view', route_name='engine_player',
                    renderer='json')

    config.scan()

    # Just set up a simple game and engine.
    buffer_engines = 1

    # from bicycle.player import Player
    from bicycle.engine import Engine
    from bicycle.blackjack.game import StandardBlackjack

    engines = {util.random_filename(16): Engine(StandardBlackjack(num_seats=6,
                                                                  face_up=True))
                    for _ in range(buffer_engines)}

    config.add_settings({'engines': engines})

    for _, engine in engines.items():
        engine.start()

    return config.make_wsgi_app()
