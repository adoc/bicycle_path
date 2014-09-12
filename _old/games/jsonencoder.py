import json

from ..cards import Card
from ..tables import Player, Hand

class Encoder(json.JSONEncoder):
    def default(self,cls):
        if isinstance(cls, Player):
            return cls.serialize()
        elif isinstance(cls, Card):
            return cls.serialize()
        elif isinstance(cls, Hand):
            return cls.serialize()
            #return cls.__repr__()
        else:
            print "No JSON encoder for type %s"%type(cls)