"""
"""

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


class WagerGameState(bicycle.game.GameState):
    __table__ = WagerTable


class TestGameStep(unittest.TestCase):
    def test_class(self):
        self.assertEqual(bicycle.game.GameStep.__timeout__, 0)
        self.assertEqual(bicycle.game.GameStep.__persistent_keys__,
                         ['timeout', 'table'])
        self.assertEqual(bicycle.game.GameStep.__view_keys__,
                         ['timeout', 'table'])

    def test_init(self):
        self.assertRaises(AssertionError, lambda: bicycle.game.GameStep(None))

        e1 = bicycle.engine.Engine(bicycle.game.GameState())
        gs1 = bicycle.game.GameStep(e1)

        self.assertIs(gs1.engine, e1)
        self.assertIs(gs1.table, e1.table)
        self.assertIs(gs1.state, e1.state)
        self.assertEqual(gs1.timeout, gs1.__timeout__)

    def test_call(self):
        e1 = bicycle.engine.Engine(bicycle.game.GameState())
        gs1 = bicycle.game.GameStep(e1)

        self.assertRaises(NotImplementedError, gs1)


class TestSittableGameStep(unittest.TestCase):
    def test_sit(self):
        p1 = bicycle.player.Player()
        p2 = bicycle.player.Player()
        e1 = bicycle.engine.Engine(bicycle.game.GameState())
        gs1 = SittableGameStep(e1)

        self.assertTrue(gs1.sit(p1))
        self.assertTrue(gs1.sit(p2))

        self.assertIs(gs1.table.to_sit[0], p1)
        self.assertIs(gs1.table.to_sit[1], p2)

        self.assertFalse(gs1.sit(p1))
        gs1.table.prepare()
        self.assertFalse(gs1.sit(p1))

    def test_leave(self):
        p1 = bicycle.player.Player()
        p2 = bicycle.player.Player()
        p3 = bicycle.player.Player()
        e1 = bicycle.engine.Engine(bicycle.game.GameState())
        gs1 = SittableGameStep(e1)

        gs1.sit(p1)
        gs1.sit(p2)
        gs1.table.prepare()
        gs1.sit(p3)

        self.assertTrue(gs1.leave(p1))
        self.assertTrue(gs1.leave(p2))
        self.assertTrue(gs1.leave(p3))

        self.assertIn(p1, gs1.table.to_leave)
        self.assertIn(p2, gs1.table.to_leave)
        self.assertNotIn(p3, gs1.table.to_sit)


class TestWagerGameStep(unittest.TestCase):
    def test_wager(self):
        # Nothing yet substantial to test.
        pass


class TestPrepareStep(unittest.TestCase):
    def test_init(self):
        e1 = bicycle.engine.Engine(bicycle.game.GameState())
        gs1 = bicycle.game.PrepareStep(e1)

        self.assertTrue(hasattr(gs1, 'sit'))
        self.assertTrue(hasattr(gs1, 'leave'))

    def test_call(self):
        p1 = bicycle.player.Player()
        e1 = bicycle.engine.Engine(bicycle.game.GameState())

        gs1 = bicycle.game.PrepareStep(e1)

        self.assertFalse(gs1())

        gs1.sit(p1)

        self.assertTrue(gs1())


class TestWagerStep(unittest.TestCase):
    def test_init(self):
        e1 = bicycle.engine.Engine(WagerGameState())
        gs1 = bicycle.game.WagerStep(e1)

        self.assertTrue(hasattr(gs1, 'sit'))
        self.assertTrue(hasattr(gs1, 'leave'))
        self.assertTrue(hasattr(gs1, 'wager'))

    def test_call(self):
        t1 = WagerTable()
        p1 = bicycle.player.Player(bankroll=10000)

        e1 = bicycle.engine.Engine(WagerGameState())
        gs1 = bicycle.game.WagerStep(e1)

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


# (c) 2011-2014 StudioCoda & Nicholas Long. All Rights Reserved