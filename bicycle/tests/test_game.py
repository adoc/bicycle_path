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
        self.assertEqual(bicycle.game.GameStep.to_execute, True)

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
        p1 = bicycle.player.Player(bankroll=100)
        p2 = bicycle.player.Player(bankroll=100)
        e1 = bicycle.engine.Engine(WagerGameState())
        gs1 = WagerGameStep(e1)

        gs1.table.sit(p1)
        gs1.table.sit(p2)
        gs1.table.prepare()

        gs1.wager(p1, 100)
        gs1.wager(p2, 100)

        self.assertEqual(gs1.table.to_wager[p1], 100)
        self.assertEqual(gs1.table.to_wager[p2], 100)

        self.assertRaises(bicycle.table.InsufficientBankroll,
                            lambda: gs1.wager(p1, 100))


class TestPrepareStep(unittest.TestCase):
    def test_class(self):
        self.assertEqual(bicycle.game.PrepareStep.__timeout__, 0)
        self.assertEqual(bicycle.game.PrepareStep.to_execute, True)

    def test_init(self):
        e1 = bicycle.engine.Engine(bicycle.game.GameState())
        gs1 = bicycle.game.PrepareStep(e1)

        self.assertTrue(hasattr(gs1, 'sit'))
        self.assertTrue(hasattr(gs1, 'leave'))

    def test_call(self):
        e1 = bicycle.engine.Engine(bicycle.game.GameState())
        gs1 = bicycle.game.PrepareStep(e1)
        p1 = bicycle.player.Player()
        p2 = bicycle.player.Player()

        self.assertFalse(gs1())
        gs1.sit(p1)
        self.assertTrue(gs1())


class TestWagerStep(unittest.TestCase):
    def test_class(self):
        self.assertIs(bicycle.game.WagerStep.__timeout__, 5)
        self.assertIs(bicycle.game.WagerStep.to_execute, True)

    def test_init(self):
        e1 = bicycle.engine.Engine(WagerGameState())
        gs1 = bicycle.game.WagerStep(e1)

        self.assertTrue(hasattr(gs1, 'sit'))
        self.assertTrue(hasattr(gs1, 'leave'))
        self.assertTrue(hasattr(gs1, 'wager'))

    def test_call(self):
        e1 = bicycle.engine.Engine(WagerGameState())
        gs1 = bicycle.game.WagerStep(e1)
        p1 = bicycle.player.Player(bankroll=10000)

        self.assertFalse(gs1())
        gs1.sit(p1)
        self.assertFalse(gs1())
        gs1.wager(p1, 1000)
        self.assertTrue(gs1())


class TestDealStep(unittest.TestCase):
    def test_class(self):
        self.assertIs(bicycle.game.DealStep.__timeout__, 0)
        self.assertIs(bicycle.game.DealStep.to_execute, True)

    def test_init(self):
        pass

    def test_call(self):
        pass


class TestPlayerStep(unittest.TestCase):
    def test_class(self):
        self.assertIs(bicycle.game.PlayerStep.__timeout__, 15)
        self.assertIs(bicycle.game.PlayerStep.to_execute, True)

    def test_init(self):
        pass

    def test_next(self):
        pass

    def test_call(self):
        pass


class TestResolveStep(unittest.TestCase):
    def test_class(self):
        self.assertIs(bicycle.game.ResolveStep.__timeout__, 10)
        self.assertIs(bicycle.game.ResolveStep.to_execute, True)


class TestCleanupStep(unittest.TestCase):
    def test_class(self):
        self.assertIs(bicycle.game.ResolveStep.__timeout__, 10)
        self.assertIs(bicycle.game.ResolveStep.to_execute, True)


class TestGameState(unittest.TestCase):
    def test_class(self):
        self.assertEqual(bicycle.game.GameState.__game__, [])
        self.assertIs(bicycle.game.GameState.__table__, bicycle.table.Table)


# (c) 2011-2014 StudioCoda & Nicholas Long. All Rights Reserved