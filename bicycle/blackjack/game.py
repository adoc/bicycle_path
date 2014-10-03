"""
"""

import itertools

import bicycle.blackjack.card

import bicycle.game

from bicycle.game import (GameState, GameStep, SittableGameStepMixin, WagerGameStepMixin, PrepareStep, WagerStep, DealStep, PlayerStep, ResolveStep, CleanupStep)


# Allow betting during the prep step.
class PrepareStep(bicycle.game.WagerGameStepMixin, bicycle.game.PrepareStep):
    def __init__(self, *args, **kwa):
        bicycle.game.PrepareStep.__init__(self, *args, **kwa)
        bicycle.game.WagerGameStepMixin.__init__(self)


class InsuranceStep(bicycle.game.GameStep):
    """
    """

    __timeout__ = 10

    @property
    def to_execute(self):
        return self.table.dealer_hand[1] == bicycle.blackjack.card.ace

    def insurance(self, player, amount):
        pass

    def __call__(self):
        pass


class PlayerStep(bicycle.game.PlayerStep):
    """
    """

    __timeout__ = 15

    def __init__(self, table):
        bicycle.game.PlayerStep.__init__(self, table)
        # Iterate through players.
        self._play_all = table._play_all_iter()
        self._player, self._hand = self._play_all.next()

    @property
    def to_execute(self):
        """If the dealer does not have a blackjack, we continue.
        """

        return not self.table.dealer_hand.blackjack

    @property
    def _stop_hand(self):
        return self._hand.blackjack or self._hand.busted

    def _next(self):
        try:
            self._player, self._hand = self._play_all.next()
            
            return True
        except StopIteration:
            return False

    def hit(self, player):
        """
        """

        if self._stop_hand is True:
            self._next()

    def stand(self, player):
        """
        """

        self._next()

    def double(self, player):
        """
        """
        raise NotImplementedError()
        self._next()


    def split(self, player):
        """
        """

        raise NotImplementedError()

    def surrender(self, player):
        """
        """

        raise NotImplementedError()

    def __call__(self):

        # Simply skip the player if delay
        return not self._next()


class ResolveStep(bicycle.game.ResolveStep):
    """
    """

    def __call__(self):

        return True


class StandardBlackjack(bicycle.game.GameState):
    """
    """

    # The Engine will use these wisely.
    __game__ = (PrepareStep, WagerStep, DealStep, InsuranceStep, PlayerStep,
                ResolveStep, CleanupStep)