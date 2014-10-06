import os
import math
import base64
import hashlib


def random_filename(length):
    assert length<=16
    randstr = base64.b64encode(
                hashlib.sha256(
                    os.urandom(length ** 2))
                .digest(), altchars=b"_-")

    def no_dash(randstr, inc):
        if randstr[inc:].startswith(b'-'):
            inc += 1
            no_dash(randstr, inc)
        return randstr

    return no_dash(randstr, 0)[: length].decode()