"""
"""

import unittest
import itertools

import bicycle.game
import bicycle.engine


class TestEngine(unittest.TestCase):
    def test_init(self):
        g1 = bicycle.game.GameState()
        e1 = bicycle.engine.Engine(g1)

        self.assertIs(e1.state, g1)
        self.assertIs(e1.table, g1.table)

        self.assertTrue(isinstance(e1.game_steps, itertools.cycle))
        
        # self.assertIsNone(e1.game)
        # self.assertIsNone(e1.timer)
        # self.assertIsNone(e1.result)

        # self.assertFalse(e1.alive)

    def test_execute_step(self):
        assert False, "Should be test code here."

    def test_set_timer(self):
        assert False, "Should be test code here."

    def test_handler(self):
        assert False, "Should be test code here."

    def test_run(self):
        assert False, "Should be test code here."

    def test_stop(self):
        assert False, "Should be test code here."


# (c) 2011-2014 StudioCoda & Nicholas Long. All Rights Reserved