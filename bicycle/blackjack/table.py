"""
"""

import bicycle.player
import bicycle.table
import bicycle.blackjack.card


class BlackjackTable(bicycle.table.WagerTableMixin,
                     bicycle.table.CardTable):
    """
    """

    __view_keys__ = (bicycle.table.WagerTableMixin.__view_keys__ +
                     bicycle.table.CardTable.__view_keys__ +
                     ['dealer', 'dealer_hand', 'insurance_wagers'])

    def __init__(self, num_seats=6,
                 dealer=bicycle.player.Player(bankroll=100000000),
                 reshuffle_threshold=0.2, face_up=False, 
                 wager_cls=bicycle.table.Wager, **kwa):
        """
        """
        self.win_payout = 1
        self.bj_payout = 1.5

        assert num_seats <= 6, "Too many seats."
        assert isinstance(dealer, bicycle.player.Player)
        bicycle.table.CardTable.__init__(self, num_seats=num_seats,
                           reshuffle_threshold=reshuffle_threshold,
                           card_cls=bicycle.blackjack.card.Card,
                           hand_cls=bicycle.blackjack.card.Hand,
                           seats_cls=bicycle.table.Seats, **kwa)
        bicycle.table.WagerTableMixin.__init__(self, num_seats=num_seats,
                                               wager_cls=wager_cls,
                                               seats_cls=bicycle.table.Seats,
                                               **kwa)

        # These can become props on Table. `sit` a dealer here in
        #   __init__ instead.
        self.dealer = dealer
        self.dealer_hand = bicycle.blackjack.card.Hand()

        # How can this be more easily implemented using WagerTableMixin?
        #   It's just a side bet and many games have such a concept.
        self.insurance_wagers = bicycle.table.Seats(num_seats,
                                                    base_obj_factory=wager_cls)

        self.face_up = face_up

    def __iter__(self):
        for seat, hand, wager, insurance in zip(self.seats, self.hands,
                                        self.wagers, self.insurance_wagers):
            yield seat, hand, wager, insurance

    def deal(self, hand, **opts):
        opts['up'] = self.face_up
        bicycle.table.CardTable.deal(self, hand, **opts)

    def _deal_all_iter(self):
        """
        """

        for player, hand, wager, _ in self:
            if player and wager:
                yield hand, {'up': self.face_up}
        yield self.dealer_hand, {'up': False}

        for player, hand, wager, _ in self:
            if player and wager:
                yield hand, {'up': self.face_up}
        yield self.dealer_hand, {'up': True}

    def _play_all_iter(self):
        """
        """

        for player, hand, wager, _ in self:
            if player and wager:
                yield player, hand, wager

    def resolve(self):
        for player, hand, wager in self._play_all_iter():
            if hand.blackjack is True and self.dealer_hand.blackjack is not True:
                print("BJ WIN!")
                wager *= 1 + self.bj_payout
            elif hand > self.dealer_hand:
                print("WIN")
                wager *= 1 + self.win_payout
            elif hand < self.dealer_hand or hand.busted:
                print("LOSE")
                self.collect_wager_func(self.dealer, wager)
            else:
                print("PUSH")

    def cleanup(self):
        """
        """

        self.dealer_hand.discard(self.discard)

        for player, _, _, insurance in self:
            if player and insurance:
                self.collect_wager_func(player, insurance.amount)
                insurance.amount = 0

        super(BlackjackTable, self).cleanup()


# (c) 2011-2014 StudioCoda & Nicholas Long. All Rights Reserved