"""
"""

import itertools

import bicycle.blackjack.card

from bicycle.game import (GameState, GameStep, SittableGameStepMixin, WagerGameStepMixin, PrepareStep, WagerStep, DealStep, PlayerStep, ResolveStep, CleanupStep)


# Allow betting during the prep step.
class PrepareStep(WagerGameStepMixin, PrepareStep):
    def __init__(self, *args, **kwa):
        PrepareStep.__init__(self, *args, **kwa)
        WagerGameStepMixin.__init__(self)


class InsuranceStep(GameStep):
    """
    """

    timeout = 10

    @property
    def execute(self):
        return self.table.dealer_hand[1] is bicycle.blackjack.card.ace

    def insurance(self, player, amount):
        pass

    def __call__(self):
        pass


class PlayerStep(PlayerStep):
    """
    """

    timeout = 15

    @property
    def execute(self):
        """If the dealer does not have a blackjack, we continue.
        """

        return not self.table.dealer_hand.blackjack

    def hit(self, player):
        """
        """

        pass

    def stand(self, player):
        """
        """

        pass

    def double(self, player):
        """
        """

        pass

    def split(self, player):
        """
        """

        pass

    def surrender(self, player):
        """
        """

        pass


class ResolveStep(ResolveStep):
    """
    """

    pass


class StandardBlackjack(GameState):
    """
    """

    # The Engine will use these wisely.
    __game__ = (PrepareStep, WagerStep, DealStep, InsuranceStep, PlayerStep,
                ResolveStep, CleanupStep)