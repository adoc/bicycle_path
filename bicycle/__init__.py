"""Bicycle init module.
"""


import random as _random


# Overload the ``random`` seed with os.urandom. This should provide a
#   fair bit of entropy to the card shuffling. However some care
#   should be excercised should the OS be recently booted.
# This usage works in Windows but this developer cannot ensure
#   sufficient entropy on a Windows system.
random = _random.SystemRandom()


def map_serialize(obj_iter, **kwa):
    """Map the `serialize` method of items from `obj_iter`.
    Passes keyword args.
    """

    return map(lambda obj: obj.serialize(**kwa), obj_iter)