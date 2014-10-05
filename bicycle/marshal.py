"""Marshal module.

Set of classes and functions used to marshal game state to and from
persistance as well as to and from implementated views.
"""


# One use case to be handled here is to set and handle an id attribute
#   on serializable objects. Should be a 


import collections


def _serialize(obj, **kwa):
    try:
        return obj.serialize(**kwa)
    except AttributeError:
        return obj


def _extract_keys(obj, keys):
    for key in keys:
        yield key, getattr(obj, key)


def marshal_object(obj, persist=False, get_id=False):
    """
    """

    key_list_attr = persist and '__persistent_keys__' or '__view_keys__' 
    get_id = get_id or persist

    if isinstance(obj, list) or isinstance(obj, tuple):
        def handle_list():
            for item in obj:
                yield marshal_object(item, persist, get_id)
        return list(handle_list())
    elif hasattr(obj, key_list_attr):
        def handle_dict():
            for key, subob in _extract_keys(obj, getattr(obj, key_list_attr)):
                yield key, marshal_object(subob, persist, get_id)
            if get_id is True:
                yield 'id', hash(obj)
        return dict(handle_dict())
    else:
        return _serialize(obj, snoop=persist)


# (c) 2011-2014 StudioCoda & Nicholas Long. All Rights Reserved