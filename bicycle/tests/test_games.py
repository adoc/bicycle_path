from pprint import pprint

import unittest

import bicycle.games



class TestSeats(unittest.TestCase):
    def test_init(self):
        s1 = bicycle.games.Seats(6)
        self.assertEqual(len(s1), 6)
        self.assertTrue(all([item is None for item in s1]))

        s1 = bicycle.games.Seats(60)
        self.assertEqual(len(s1), 60)
        self.assertTrue(all([item is None for item in s1]))

    def test_init_base_obj(self):
        s1 = bicycle.games.Seats(6, base_obj_factory=lambda: [])
        self.assertEqual(len(s1), 6)
        self.assertTrue(all([item == [] for item in s1]))

        s1 = bicycle.games.Seats(60, base_obj_factory=lambda: [])
        self.assertEqual(len(s1), 60)
        self.assertTrue(all([item == [] for item in s1]))

    def test_remove(self):
        s1 = bicycle.games.Seats(6)
        s1.remove(None)
        s1.remove(None)
        s1.remove(None)
        s1.remove(None)
        s1.remove(None)
        s1.remove(None)
        self.assertEqual(len(s1), 6)
        self.assertTrue(all([item is None for item in s1]))

        s1[0] = True
        s1[2] = False
        s1.remove(True)
        s1.remove(False)
        self.assertEqual(len(s1), 6)
        self.assertTrue(all([item is None for item in s1]))

        self.assertRaises(ValueError, lambda: s1.remove(True))
        self.assertRaises(ValueError, lambda: s1.remove(False))

    def test_remove_base_obj(self):
        s1 = bicycle.games.Seats(6, base_obj_factory=lambda: [])
        s1.remove([])
        s1.remove([])
        s1.remove([])
        s1.remove([])
        s1.remove([])
        s1.remove([])
        self.assertEqual(len(s1), 6)
        self.assertTrue(all([item == [] for item in s1]))

        s1[0] = True
        s1[2] = False
        s1.remove(True)
        s1.remove(False)
        self.assertEqual(len(s1), 6)
        self.assertTrue(all([item == [] for item in s1]))

        self.assertRaises(ValueError, lambda: s1.remove(True))
        self.assertRaises(ValueError, lambda: s1.remove(False))

    def test_insert(self):
        s1 = bicycle.games.Seats(6)
        s1.insert(0, True)
        s1.insert(2, False)

        self.assertEqual(len(s1), 6)
        self.assertEqual([item is None for item in s1].count(True), 4)

        s2 = bicycle.games.Seats(6)
        s1.insert(None, True)
        s1[1] = True
        s1.insert(None, False)
        self.assertEqual(len(s1), 6)
        self.assertEqual(s1[0], True)
        self.assertEqual(s1[1], True)
        self.assertEqual(s1[2], False)

    def test_insert_base_obj(self):
        s1 = bicycle.games.Seats(6, base_obj_factory=lambda: [])
        s1.insert(0, True)
        s1.insert(2, False)

        self.assertEqual(len(s1), 6)
        self.assertEqual([item == [] for item in s1].count(True), 4)

        s2 = bicycle.games.Seats(6, base_obj_factory=lambda: [])
        s1.insert(None, True)
        s1[1] = True
        s1.insert(None, False)
        self.assertEqual(len(s1), 6)
        self.assertEqual(s1[0], True)
        self.assertEqual(s1[1], True)
        self.assertEqual(s1[2], False)


class TestPlayer(unittest.TestCase):
    def test_init(self):
        pass


class TestTable(unittest.TestCase):
    def test_init(self):
        t1 = bicycle.games.Table()
        self.assertEqual(len(t1.seats), 6)
        self.assertEqual(t1.to_play, [])
        self.assertIsInstance(t1.seats, bicycle.games.Seats)

    def test_sit(self):
        t1 = bicycle.games.Table()
        p1 = bicycle.games.Player()
        p2 = bicycle.games.Player()
        p3 = bicycle.games.Player()
        p4 = bicycle.games.Player()
        p5 = bicycle.games.Player()
        p6 = bicycle.games.Player()
        p7 = bicycle.games.Player()

        t1.sit(p1)
        t1.sit(p2, index=5)
        self.assertEqual(t1.seat_prefs[p2], 5)

        t1.sit(p3, index=0) # Someone already in that position.
        self.assertEqual(t1.seat_prefs[p3], 0)

        t1.sit(p4)
        t1.sit(p5)
        t1.sit(p6)

        self.assertEqual(t1.to_play, [p1, p2, p3, p4, p5, p6])

        # This may move to the "cleanup test"
        t1.cleanup()
        t1.sit(p7)
        self.assertIn(p7, t1.to_play)

        self.assertEqual(t1.seats[0], p1)
        self.assertEqual(t1.seats[5], p2)
        self.assertEqual(t1.seats[1], p3)
        self.assertEqual(t1.seats[2], p4)
        self.assertEqual(t1.seats[3], p5)
        self.assertEqual(t1.seats[4], p6)
        

    def test_leave(self):
        t1 = bicycle.games.Table()
        p1 = bicycle.games.Player()
        p2 = bicycle.games.Player()
        p3 = bicycle.games.Player()
        p4 = bicycle.games.Player()
        p5 = bicycle.games.Player()
        p6 = bicycle.games.Player()
        p7 = bicycle.games.Player()

        t1.seats = bicycle.games.Seats([p1, p2, p3, p4, p5, p6])
        t1.to_play = [p7]

        t1.leave(p7)
        self.assertNotIn(p7, t1.to_play)

        t1.cleanup()
        t1.leave(p6)
        t1.leave(p5)
        t1.leave(p4)
        self.assertEqual(t1.to_leave, [p6, p5, p4])

        t1.cleanup()
        self.assertNotIn(p6, t1.seats)
        self.assertNotIn(p5, t1.seats)
        self.assertNotIn(p4, t1.seats)

    def test_resolve(self):
        t1 = bicycle.games.Table()
        self.assertRaises(NotImplementedError, t1.resolve)

    def test_cleanup(self):
        t1 = bicycle.games.Table()
        p1 = bicycle.games.Player()
        p2 = bicycle.games.Player()
        p3 = bicycle.games.Player()
        p4 = bicycle.games.Player()

        t1.seats = bicycle.games.Seats([p1, p2, p3, None])
        t1.to_play = [p4]

        t1.cleanup()
        self.assertIn(p4, t1.seats)


class TestWager(unittest.TestCase):
    def test_init(self):
        w1 = bicycle.games.Wager()
        self.assertEqual(w1.amount, 0)

        w2 = bicycle.games.Wager(amount=1)
        self.assertEqual(w2.amount, 1)

    def test_bool(self):
        w1 = bicycle.games.Wager()
        self.assertFalse(w1)

        w2 = bicycle.games.Wager(amount=0.1)
        self.assertTrue(w2)

    def test_lt(self):
        w1 = bicycle.games.Wager(amount=10)
        w2 = bicycle.games.Wager(amount=5)
        self.assertLess(w2, w1)
        self.assertLess(1, w1)
        self.assertLess(1, w2)

    def test_gt(self):
        w1 = bicycle.games.Wager(amount=10)
        w2 = bicycle.games.Wager(amount=5)
        self.assertGreater(w1, w2)
        self.assertGreater(w1, 1)
        self.assertGreater(w2, 1)

    def test_eq(self):
        w1 = bicycle.games.Wager(amount=10)
        w2 = bicycle.games.Wager(amount=10)
        self.assertEqual(w1, w2)
        self.assertEqual(w1, 10)
        self.assertEqual(w2, 10)


class TestCardTable(unittest.TestCase):
    def test_init(self):
        t1 = bicycle.games.CardTable()

        self.assertEqual(t1.hands, bicycle.games.Seats(t1.num_seats, base_obj_factory=bicycle.cards.Cards))
        #self.assertEqual(t1.wagers, bicycle.games.Seats(t1.num_seats, base_obj=0)
        self.assertTrue(not any(t1.wagers))
        self.assertEqual(t1.shoe, bicycle.cards.Cards())
        self.assertEqual(t1.discard, bicycle.cards.Cards())
        self.assertEqual(t1.wager_func, bicycle.games.wager)
        self.assertEqual(t1.collect_func, bicycle.games.collect)
        self.assertEqual(t1.to_wager, {})

    def test_leave(self):
        t1 = bicycle.games.CardTable()

        p1 = bicycle.games.Player(bankroll=1000)
        t1.sit(p1)
        t1.wager(p1, 11)
        t1.leave(p1)

        self.assertNotIn(p1, t1.to_wager)

    # Functional test?? Move this!
    def test_state_scenario_one(self):
        t1 = bicycle.games.CardTable()

        p1 = bicycle.games.Player(bankroll=1000)
        p2 = bicycle.games.Player(bankroll=1000)
        p3 = bicycle.games.Player(bankroll=1000)
        p4 = bicycle.games.Player(bankroll=1000)

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

        self.assertEqual(t1.to_wager, {})
        self.assertEqual(t1.seat_prefs, {})
        self.assertEqual(t1.seats, [p1, p2, p4, None, None, None])

        self.assertEqual(t1.wagers[0], 11)
        self.assertEqual(t1.wagers[1], 12)
        self.assertEqual(t1.wagers[2], 14)

        # HERE!
        # pprint(t1.__dict__)
        # assert False

    def test_iter(self):
        pass

    def test_build(self):
        t1 = bicycle.games.CardTable()

        t1.build()
        self.assertEqual(len(t1.shoe), 52)
        self.assertEqual(t1.shoe[0], bicycle.cards.Card(suit=0, rank=0))

    def test_pickup(self):
        t1 = bicycle.games.CardTable()

        t1.build()
        bicycle.cards.deal_all(t1.shoe, t1.discard)
        self.assertEqual(len(t1.shoe), 0)
        self.assertEqual(len(t1.discard), 52)
        self.assertEqual(t1.discard[0], bicycle.cards.Card(suit=3, rank=12))

        t1.pickup()
        self.assertEqual(len(t1.shoe), 52)
        self.assertEqual(len(t1.discard), 0)
        self.assertEqual(t1.shoe[0], bicycle.cards.Card(suit=0, rank=0))

    def test_shuffle(self):
        t1 = bicycle.games.CardTable()

        t1.build()
        t1.shuffle()
        self.assertEqual(len(t1.shoe), 52)
        try:
            self.assertNotEqual(t1.shoe[0], bicycle.cards.Card(suit=0, rank=0))
        except AssertionError:
            self.assertNotEqual(t1.shoe[1], bicycle.cards.Card(suit=0, rank=1))

    def test_deal_all(self):
        t1 = bicycle.games.CardTable()
        p1 = bicycle.games.Player()
        p2 = bicycle.games.Player()
        p3 = bicycle.games.Player()

        t1.build()


    def test_cleanup(self):
        # Not complete.
        p1 = bicycle.games.Player()
        p2 = bicycle.games.Player()
        p3 = bicycle.games.Player()
        p4 = bicycle.games.Player()

        t1 = bicycle.games.CardTable()

        t1.sit(p1)
        t1.sit(p2)
        t1.sit(p3)
        t1.sit(p4)
        t1.cleanup()


