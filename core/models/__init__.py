from typing import List


class Serialize:
    def __init__(self, *keys: List[str]):
        self.keys = keys

    def serialize(self):
        def _serialize(item):
            if isinstance(item, Serialize):
                return item.serialize()
            elif isinstance(item, (list, tuple)):
                return tuple(map(_serialize, item))
            elif isinstance(item, dict):
                return item
            return item

        return {
            key: _serialize(getattr(self, key))
            for key in self.keys
        }
