import unittest

import bicycle.player
import bicycle.table
import bicycle.game


# Set up some classes used in testing.
class SittableGameStep(bicycle.game.SittableGameStepMixin, bicycle.game.GameStep):
    def __init__(self, *args, **kwa):
        bicycle.game.GameStep.__init__(self, *args, **kwa)
        bicycle.game.SittableGameStepMixin.__init__(self)


class WagerGameStep(bicycle.game.WagerGameStepMixin, bicycle.game.GameStep):
    def __init__(self, *args, **kwa):
        bicycle.game.GameStep.__init__(self, *args, **kwa)
        bicycle.game.WagerGameStepMixin.__init__(self)


class WagerTable(bicycle.table.WagerTableMixin, bicycle.table.Table):
    def __init__(self):
        bicycle.table.Table.__init__(self)
        bicycle.table.WagerTableMixin.__init__(self)


class TestGameStep(unittest.TestCase):
    def test_init(self):
        self.assertRaises(AssertionError, lambda: bicycle.game.GameStep(None))

        t1 = bicycle.table.Table()
        gs1 = bicycle.game.GameStep(t1)

        self.assertIs(gs1.table, t1)

    def test_call(self):
        t1 = bicycle.table.Table()
        gs1 = bicycle.game.GameStep(t1)

        self.assertRaises(NotImplementedError, gs1)


class TestSittableGameStepMixin(unittest.TestCase):
    def test_sit(self):
        p1 = bicycle.player.Player()
        p2 = bicycle.player.Player()
        t1 = bicycle.table.Table()
        gs1 = SittableGameStep(t1)

        self.assertTrue(gs1.sit(p1))
        self.assertTrue(gs1.sit(p2))

        self.assertIs(gs1.table.to_play[0], p1)
        self.assertIs(gs1.table.to_play[1], p2)

        self.assertFalse(gs1.sit(p1))
        gs1.table.prepare()
        self.assertFalse(gs1.sit(p1))

    def test_leave(self):
        p1 = bicycle.player.Player()
        p2 = bicycle.player.Player()
        p3 = bicycle.player.Player()
        t1 = bicycle.table.Table()
        gs1 = SittableGameStep(t1)

        gs1.sit(p1)
        gs1.sit(p2)
        gs1.table.prepare()
        gs1.sit(p3)

        self.assertTrue(gs1.leave(p1))
        self.assertTrue(gs1.leave(p2))
        self.assertTrue(gs1.leave(p3))

        self.assertIn(p1, gs1.table.to_leave)
        self.assertIn(p2, gs1.table.to_leave)
        self.assertNotIn(p3, gs1.table.to_play)


class TestWagerGameStepMixin(unittest.TestCase):
    def test_wager(self):
        # Nothing yet substantial to test.
        pass


class TestPrepareStep(unittest.TestCase):
    def test_init(self):
        t1 = bicycle.table.Table()
        gs1 = bicycle.game.PrepareStep(t1)

        self.assertTrue(hasattr(gs1, 'sit'))
        self.assertTrue(hasattr(gs1, 'leave'))

    def test_call(self):
        t1 = bicycle.table.Table()
        p1 = bicycle.player.Player()
        gs1 = bicycle.game.PrepareStep(t1)

        self.assertFalse(gs1())

        gs1.sit(p1)

        self.assertTrue(gs1())


class TestWagerStep(unittest.TestCase):
    def test_init(self):
        t1 = WagerTable()
        gs1 = bicycle.game.WagerStep(t1)

        self.assertTrue(hasattr(gs1, 'sit'))
        self.assertTrue(hasattr(gs1, 'leave'))
        self.assertTrue(hasattr(gs1, 'wager'))

    def test_call(self):
        t1 = WagerTable()
        p1 = bicycle.player.Player(bankroll=10000)
        gs1 = bicycle.game.WagerStep(t1)

        self.assertFalse(gs1())
        gs1.sit(p1)
        self.assertFalse(gs1())
        gs1.wager(p1, 1000)
        self.assertTrue(gs1())


class TestDealStep(unittest.TestCase):
    pass


class TestPlayerStep(unittest.TestCase):
    pass


class ResolveStep(unittest.TestCase):
    pass


class CleanupStep(unittest.TestCase):
    pass