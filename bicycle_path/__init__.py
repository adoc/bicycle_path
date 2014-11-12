"""
"""

import gevent

from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    config.include('pyramid_mako')
    config.include('pyramid_beaker')

    config.add_static_view('static', 'static', cache_max_age=0)

    config.add_route('home', '/')
    # config.add_route('game', '/game')
    
    config.add_view('bicycle_path.views.meta_view', route_name='home',
                    renderer='templates/game.html.mako')

    # SocketIO
    config.add_route('socket_endpoint', '/api/v1/sock/*remaining')

    config.scan()

    # Just set up a simple game and engine.
    buffer_engines = 1

    # from bicycle.player import Player
    from bicycle.engine import Engine, EngineGreenlet
    from bicycle.blackjack.game import StandardBlackjack


    engines = {}
    greenlets = {}

    for _ in range(buffer_engines):
        key = util.random_filename(16)
        engine = Engine(StandardBlackjack(num_seats=6, face_up=True))
        engines.update({key: engine})
        greenlets.update({key: EngineGreenlet(engine)})

    config.add_settings({'engines': engines,
                         'greenlets': greenlets,
                         'players': {}})

    # Start the engines.
    for _, greenlet in greenlets.items():
        greenlet.start()

    return config.make_wsgi_app()