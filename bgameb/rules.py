"""Rules objects for game stuff
"""
from typing import Deque, List, Any
from dataclasses import dataclass, field
from collections import deque
from dataclasses_json import DataClassJsonMixin, config
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


@dataclass
class Stream(deque, DataClassJsonMixin):
    """Stream is a deque-like object for save
    sata about game turns

    Args:
        name (str): name of Stream.
        _order (List[Rule]): list of default elements of Stream.
    """
    name: str
    _order: List[Rule] = field(
        default_factory=list,
        repr=False,
        metadata=config(exclude=lambda x: True),
        )

    def add_rule(self, name: str, text: str):
        """Add rule to basic structure of turn
        Yhis structure is a list of Rules. The method
        new_cycle() instantiaate the turn inside
        Stream class.

        Args:
            name (str): name of phase rule
            text (str): text of phase rule
        """
        self._order.append(Rule(name=name, text=text))

    def new_cycle(self):
        """Clear the Stream and instantiate new turn
        """
        self.clear()
        self.extend(self._order)

    def __repr__(self):
        items = (f"{rule.name}={rule.text}" for rule in self)
        return "{}({})".format(self.name, ", ".join(items))
