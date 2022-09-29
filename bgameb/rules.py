"""Rules objects for game stuff
"""
from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


@dataclass(eq=True)
class Rule(dict, DataClassJsonMixin):
    """Rule collection
    """
    name: str
    is_active: bool = True

    def __getattr__(self, attr: str) -> str:
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(attr)

    def __setattr__(self, attr: str, value: str) -> None:
        self[attr] = value

    def __delattr__(self, attr: str) -> None:
        del self[attr]

    def __repr__(self):
        items = (f"{k}={v!r}" for k, v in self.items())
        return "{}({})".format(type(self).__name__, ", ".join(items))
