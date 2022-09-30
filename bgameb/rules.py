"""Rules objects for game stuff
"""
from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin
from bgameb.base import Components


@dataclass
class Rule(dict, DataClassJsonMixin):
    """Rule collection
    """
    name: str
    text: str

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


@dataclass
class RulesMixin:
    """Mixin class for classes tht needs rules"""

    rules: Components = field(default_factory=Components)

    def add_rule(self, name: str, text: str):
        """Add rule to game rules

        Args:
            name (str): name of rule
            text (str): text of rule
        """
        self.rules[name] = Rule(name=name, text=text)
