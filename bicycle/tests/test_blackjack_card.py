"""Blackjack Cards module Unit Tests.
"""


import unittest

import bicycle.card
import bicycle.blackjack.card


class TestBlackjackCard(unittest.TestCase):
    def test_int(self):
        # Check ALL card values.
        c1 = bicycle.blackjack.card.Card.from_str("AS")
        c2 = bicycle.blackjack.card.Card.from_str("2C")
        c3 = bicycle.blackjack.card.Card.from_str("3D")
        c4 = bicycle.blackjack.card.Card.from_str("4H")
        c5 = bicycle.blackjack.card.Card.from_str("5S")
        c6 = bicycle.blackjack.card.Card.from_str("6C")
        c7 = bicycle.blackjack.card.Card.from_str("7D")
        c8 = bicycle.blackjack.card.Card.from_str("8H")
        c9 = bicycle.blackjack.card.Card.from_str("9S")
        ca = bicycle.blackjack.card.Card.from_str("10C")
        cb = bicycle.blackjack.card.Card.from_str("JD")
        cc = bicycle.blackjack.card.Card.from_str("QH")
        cd = bicycle.blackjack.card.Card.from_str("KS")

        self.assertEqual(int(c1), 1)
        self.assertEqual(int(c2), 2)
        self.assertEqual(int(c3), 3)
        self.assertEqual(int(c4), 4)
        self.assertEqual(int(c5), 5)
        self.assertEqual(int(c6), 6)
        self.assertEqual(int(c7), 7)
        self.assertEqual(int(c8), 8)
        self.assertEqual(int(c9), 9)
        self.assertEqual(int(ca), 10)
        self.assertEqual(int(cb), 10)
        self.assertEqual(int(cc), 10)
        self.assertEqual(int(cd), 10)

    def test_lt(self):
        c1 = bicycle.blackjack.card.Card.from_str("AS")
        c2 = bicycle.blackjack.card.Card.from_str("2C")
        c3 = bicycle.blackjack.card.Card.from_str("KH")
        c4 = bicycle.blackjack.card.Card.from_str("QD")

        self.assertLess(c1, c2)

        self.assertLess(c1, c3)
        self.assertLess(c1, c4)

        self.assertLess(c2, c3)
        self.assertLess(c2, c4)

    def test_gt(self):
        c1 = bicycle.blackjack.card.Card.from_str("AS")
        c2 = bicycle.blackjack.card.Card.from_str("2C")
        c3 = bicycle.blackjack.card.Card.from_str("KH")
        c4 = bicycle.blackjack.card.Card.from_str("QD")

        self.assertGreater(c4, c1)
        self.assertGreater(c4, c2)

        self.assertGreater(c3, c1)
        self.assertGreater(c3, c2)

        self.assertGreater(c2, c1)

    def test_eq(self):
        c1 = bicycle.blackjack.card.Card.from_str("AS")
        c2 = bicycle.blackjack.card.Card.from_str("AC")
        c3 = bicycle.blackjack.card.Card.from_str("2S")
        c4 = bicycle.blackjack.card.Card.from_str("2C")
        c5 = bicycle.blackjack.card.Card.from_str("10H")
        c6 = bicycle.blackjack.card.Card.from_str("KH")
        c7 = bicycle.blackjack.card.Card.from_str("QD")

        self.assertEqual(c1, c2)
        self.assertEqual(c3, c4)
        self.assertEqual(c5, c6)
        self.assertEqual(c6, c7)

    def test_ne(self):
        c1 = bicycle.blackjack.card.Card.from_str("AS")
        c2 = bicycle.blackjack.card.Card.from_str("2S")
        c3 = bicycle.blackjack.card.Card.from_str("10H")
        c4 = bicycle.blackjack.card.Card.from_str("QD")

        self.assertNotEqual(c1, c2)
        self.assertNotEqual(c2, c3)
        self.assertNotEqual(c3, c4)


class TestAce(unittest.TestCase):
    def test_ace(self):
        ace = bicycle.blackjack.card.ace

        a1 = bicycle.blackjack.card.Card.from_str("AC")
        a2 = bicycle.blackjack.card.Card.from_str("KC")

        self.assertEqual(int(ace), 1)
        self.assertEqual(ace, a1)
        self.assertNotEqual(ace, a2)


class TestHand(unittest.TestCase):
    def test_int(self):
        h1 = bicycle.blackjack.card.Hand()
        h1.append(bicycle.blackjack.card.Card.from_str("AS"))
        h1.append(bicycle.blackjack.card.Card.from_str("KS"))
        self.assertEqual(int(h1), 21)

        h2 = bicycle.blackjack.card.Hand()
        h2.append(bicycle.blackjack.card.Card.from_str("AS"))
        h2.append(bicycle.blackjack.card.Card.from_str("AS"))
        self.assertEqual(int(h2), 12)
        h2.append(bicycle.blackjack.card.Card.from_str("KS"))
        self.assertEqual(int(h2), 12)
        h2.append(bicycle.blackjack.card.Card.from_str("QC"))
        self.assertEqual(int(h2), 22)

    def test_blackjack(self):
        h1 = bicycle.blackjack.card.Hand()
        h1.append(bicycle.blackjack.card.Card.from_str("AS"))
        h1.append(bicycle.blackjack.card.Card.from_str("KS"))
        self.assertTrue(h1.blackjack)

        h2 = bicycle.blackjack.card.Hand()
        h2.append(bicycle.blackjack.card.Card.from_str("AS"))
        h2.append(bicycle.blackjack.card.Card.from_str("10H"))
        self.assertTrue(h2.blackjack)

        h3 = bicycle.blackjack.card.Hand()
        h3.append(bicycle.blackjack.card.Card.from_str("AS"))
        h3.append(bicycle.blackjack.card.Card.from_str("AH"))
        h3.append(bicycle.blackjack.card.Card.from_str("9H"))
        self.assertFalse(h3.blackjack)

    def test_busted(self):
        h1 = bicycle.blackjack.card.Hand()
        h1.append(bicycle.blackjack.card.Card.from_str("AS"))
        h1.append(bicycle.blackjack.card.Card.from_str("KS"))
        self.assertFalse(h1.busted)

        h1 = bicycle.blackjack.card.Hand()
        h1.append(bicycle.blackjack.card.Card.from_str("KS"))
        h1.append(bicycle.blackjack.card.Card.from_str("2S"))
        h1.append(bicycle.blackjack.card.Card.from_str("KS"))
        self.assertTrue(h1.busted)

class TestBuild(unittest.TestCase):
    def test_build(self):
        s1 = bicycle.card.Cards()

        s1 = bicycle.blackjack.card.Card.build()

        for c in s1:
            self.assertIsInstance(c, bicycle.blackjack.card.Card)