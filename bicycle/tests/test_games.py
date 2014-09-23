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
        t1.sit(p3, index=0) # Someone already in that position.
        t1.sit(p4)
        t1.sit(p5)
        t1.sit(p6)
        t1.cleanup()
        t1.sit(p7)
        self.assertEqual(t1.seats[0], p1)
        self.assertEqual(t1.seats[5], p2)
        self.assertEqual(t1.seats[1], p3)
        self.assertEqual(t1.seats[2], p4)
        self.assertEqual(t1.seats[3], p5)
        self.assertEqual(t1.seats[4], p6)
        self.assertIn(p7, t1.to_play)

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
        t1.cleanup()
        self.assertNotIn(p7, t1.to_play)

        t1.leave(p6)
        t1.leave(p5)
        t1.leave(p4)
        t1.cleanup()
        self.assertNotIn(p6, t1.seats)
        self.assertNotIn(p5, t1.seats)
        self.assertNotIn(p4, t1.seats)

    def test_resolve(self):
        t1 = bicycle.games.Table()
        p1 = bicycle.games.Player()
        p2 = bicycle.games.Player()
        p3 = bicycle.games.Player()
        p4 = bicycle.games.Player()

        t1.seats = bicycle.games.Seats([p1, p2, p3, None])
        t1.to_play = [p4]


        t1.cleanup()
        self.assertIn(p4, t1.seats)