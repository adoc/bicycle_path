"""
"""
# There may not continue to be a `player` module, but this needed
#   separation from the `games` module.

bankrolls = {
                1.0:        'busted',
                1000.0:     'a little light',
                10000.0:    'throwing weight',
                100000.0:   'rolling',
                1000000.0:  'whale'
            }


class Player(object):
    """
    """

    __persistent_keys__ = ['bankroll', 'seat_pref']
    __view_keys__ = ['bankroll_view']

    def __init__(self, seat_pref=None, bankroll=0):
        """Initialize a Player object.

        params
        ------
        seat_pref   (int)       This Player's prefered seating
                                position.
        bankroll    (int/float) This Player's bankroll.
        """

        self.bankroll = bankroll
        self.seat_pref = seat_pref

    @property
    def bankroll_view(self):
        bankroll_key = 1.0
        for k in bankrolls:
            if self.bankroll / k > 1.0:
                bankroll_key = max(k, bankroll_key)
        return bankrolls[bankroll_key]


# (c) 2011-2014 StudioCoda & Nicholas Long. All Rights Reserved