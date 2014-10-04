"""
"""

import random
import unittest


class TestInitModule(unittest.TestCase):
    def test_random(self):
        import bicycle
        self.assertIsInstance(bicycle.random, random.SystemRandom)

    def test_map_serialize(self):
        assert False, "Should be test code here."


# (c) 2011-2014 StudioCoda & Nicholas Long. All Rights Reserved