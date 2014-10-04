"""
"""
# There may not continue to be a `player` module, but this needed
#   separation from the `games` module.


class Player(object):
    """
    """

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

    def _seralize_iter(self, snoop=False):
        """
        """

        if snoop is True:
            if self.seat_prof is not None:
                yield 'seat_pref', self.seat_pref
            yield 'bankroll', self.bankroll

    def serialize(self, snoop=False):
        """
        """

        return dict(self._seralize_iter(snoop=snoop))

    def __json__(self):
        """Public serialization of a Player object.
        """

        return self.serialize(snoop=False)


# (c) 2011-2014 StudioCoda & Nicholas Long. All Rights Reserved