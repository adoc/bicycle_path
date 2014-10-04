"""
"""

import unittest

import bicycle.blackjack.table

from pprint import pprint

try:
    range = xrange
except NameError:
    pass


class TestBlackjackTable(unittest.TestCase):
    def test_init(self):
        t1 = bicycle.blackjack.table.BlackjackTable()

        self.assertIsInstance(t1.dealer, bicycle.player.Player)
        self.assertIsInstance(t1.dealer_hand, bicycle.blackjack.card.Hand)

        self.assertEqual(t1.reshuffle_threshold, 0.2)
        self.assertFalse(t1.face_up)

    def test_init_kwa(self):
        pass

    def test_deal_all_iter(self):
        t1 = bicycle.blackjack.table.BlackjackTable()

        p1 = bicycle.player.Player(bankroll=1000)
        p2 = bicycle.player.Player(bankroll=1000)
        p3 = bicycle.player.Player(bankroll=1000)
        p4 = bicycle.player.Player(bankroll=1000)

        t1.sit(p1)
        t1.sit(p2)
        t1.sit(p3)
        t1.sit(p4)
        t1.wager(p1, 11)
        t1.wager(p2, 12)
        t1.wager(p3, 13)
        t1.wager(p4, 14)

        t1.prepare()

        self.assertEqual(list(t1._deal_all_iter()),
            [(t1.hands[0], {'up': False}),
            (t1.hands[1], {'up': False}),
            (t1.hands[2], {'up': False}),
            (t1.hands[3], {'up': False}),
            (t1.dealer_hand, {'up': False}),
            (t1.hands[0], {'up': False}),
            (t1.hands[1], {'up': False}),
            (t1.hands[2], {'up': False}),
            (t1.hands[3], {'up': False}),
            (t1.dealer_hand, {'up': True})])

    def test_deal_all(self):
        t1 = bicycle.blackjack.table.BlackjackTable()

        p1 = bicycle.player.Player(bankroll=1000)
        p2 = bicycle.player.Player(bankroll=1000)
        p3 = bicycle.player.Player(bankroll=1000)
        p4 = bicycle.player.Player(bankroll=1000)

        t1.sit(p1)
        t1.sit(p2)
        t1.sit(p3)
        t1.sit(p4)
        t1.wager(p1, 11)
        t1.wager(p2, 12)
        t1.wager(p3, 13)
        t1.wager(p4, 14)
        t1.prepare()

        t1.deal_all()

        for hand in t1.hands[:4]:
            self.assertEqual(len(hand), 2)
        self.assertEqual(len(t1.dealer_hand), 2)

    def test_cleanup(self):
        t1 = bicycle.blackjack.table.BlackjackTable()

        p1 = bicycle.player.Player(bankroll=1000)
        p2 = bicycle.player.Player(bankroll=1000)
        p3 = bicycle.player.Player(bankroll=1000)
        p4 = bicycle.player.Player(bankroll=1000)

        t1.sit(p1)
        t1.sit(p2)
        t1.sit(p3)
        t1.sit(p4)
        t1.wager(p1, 11)
        t1.wager(p2, 12)
        t1.wager(p3, 13)
        t1.wager(p4, 14)
        t1.prepare()
        t1.deal_all()

        t1.cleanup()

        for hand in t1.hands[:4]:
            self.assertEqual(len(hand), 0)
        self.assertEqual(len(t1.dealer_hand), 0)

class TestFunctional(unittest.TestCase):
    def test_scenario_one(self):
        t1 = bicycle.blackjack.table.BlackjackTable(face_up=True)

        p1 = bicycle.player.Player(bankroll=1000)
        p2 = bicycle.player.Player(bankroll=1000)
        p3 = bicycle.player.Player(bankroll=1000)
        p4 = bicycle.player.Player(bankroll=1000)

        t1.sit(p1)
        t1.sit(p2)
        t1.sit(p3)
        t1.sit(p4)
        t1.wager(p1, 11)
        t1.wager(p2, 12)
        t1.wager(p3, 13)
        t1.wager(p4, 14)
        t1.leave(p3)
        
        t1.cleanup()
        t1.prepare()

        t1.deal_all()

        t1.cleanup()

        pprint(t1.hands[0].serialize())
        pprint(t1.dealer_hand.serialize())

        #assert False


# (c) 2011-2014 StudioCoda & Nicholas Long. All Rights Reserved