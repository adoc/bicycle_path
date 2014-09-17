import unittest
import bicycle.cards


class TestCardClass(unittest.TestCase):

    def test_init(self):
        c = bicycle.cards.Card(suit=0, rank=0, up=True, private=False)

        self.assertEqual(c.suit, 0)
        self.assertEqual(c.rank, 0)
        self.assertFalse(c.private)
        self.assertTrue(c.up)

    def test_from_str(self):
        c = bicycle.cards.Card.from_str('AC')

        self.assertEqual(c.rank, 0)
        self.assertEqual(c.suit, 2)

        c = bicycle.cards.Card.from_str('AS')

        self.assertEqual(c.rank, 0)
        self.assertEqual(c.suit, 0)

        c = bicycle.cards.Card.from_str('AS', up=True, private=False)

        self.assertEqual(c.suit, 0)
        self.assertEqual(c.rank, 0)
        self.assertFalse(c.private)
        self.assertTrue(c.up)

    def test_eq(self):
        c1 = bicycle.cards.Card.from_str('AS')
        c2 = bicycle.cards.Card.from_str('AS')
        self.assertEqual(c1, c2)

        c5 = bicycle.cards.Card.from_str('KS')
        self.assertNotEqual(c1, c5)

    def test_serialize(self):
        c = bicycle.cards.Card.from_str('AS')

        self.assertEqual(c.serialize(), 'XX')
        self.assertEqual(c.serialize(snoop=True), 'AS')

        c = bicycle.cards.Card.from_str('KC', up=True)

        self.assertEqual(c.serialize(), 'KC')

    def test_json(self):
        pass

    def test_iter(self):
        pass

    def test_repr(self):
        pass


class TestDeckClass(unittest.TestCase):
    pass


class TestShoeClass(unittest.TestCase):
    pass