"""
"""

import bicycle.player
import bicycle.table
import bicycle.blackjack.card


class BlackjackTable(bicycle.table.WagerTableMixin,
                     bicycle.table.CardTable):
    """
    """

    def __init__(self, num_seats=6, dealer=bicycle.player.Player(),
                 reshuffle_threshold=0.2, face_up=False, **kwa):
        """
        """

        assert num_seats <= 6, "Too many seats."
        assert isinstance(dealer, bicycle.player.Player)
        bicycle.table.CardTable.__init__(self, num_seats=num_seats,
                           card_cls=bicycle.blackjack.card.Card,
                           hand_cls=bicycle.blackjack.card.Hand, **kwa)
        bicycle.table.WagerTableMixin.__init__(self, num_seats=num_seats,
                                               **kwa)

        self.dealer = dealer
        self.dealer_hand = bicycle.blackjack.card.Hand()

        self.reshuffle_threshold = reshuffle_threshold
        self.face_up = face_up

    def _deal_all_iter(self):
        """
        """

        for player, hand, wager in self:
            if player and wager:
                yield hand, {'up': self.face_up}
        yield self.dealer_hand, {'up': False}

        for player, hand, wager in self:
            if player and wager:
                yield hand, {'up': self.face_up}
        yield self.dealer_hand, {'up': True}

    def cleanup(self):
        """
        """

        self.dealer_hand.discard(self.discard)

        super(BlackjackTable, self).cleanup()