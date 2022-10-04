"""Rules objects for game stuff
"""
from typing import List, Literal
from dataclasses import dataclass, field
from collections import deque
from dataclasses_json import DataClassJsonMixin, config
from bgameb.base import Base, Components


@dataclass
class Rule(Components, DataClassJsonMixin):
    """Rule object
    """
    name: str
    text: str
    is_active: bool = True

    # def __getattr__(self, attr: str) -> str:
    #     try:
    #         return self[attr]
    #     except KeyError:
    #         raise AttributeError(attr)

    # def __setattr__(self, attr: str, value: str) -> None:
    #     self[attr] = value

    # def __delattr__(self, attr: str) -> None:
    #     del self[attr]

    # def __repr__(self):
    #     items = (f"{k}={v!r}" for k, v in self.items())
    #     return "{}({})".format(type(self).__name__, ", ".join(items))


# @dataclass
# class Rules(Base, DataClassJsonMixin):
#     """_summary_
#     """
#     def __post_init__(self) -> None:
#         super().__post_init__()


# @dataclass
# class RulesMixin(DataClassJsonMixin):
#     """Mixin class for classes tht needs rules"""

#     rules: Components = field(default_factory=Components)

#     def add_phase(self, name: str, text: str):
#         """Add rule to game rules

#         Args:
#             name (str): name of rule
#             text (str): text of rule
#         """
#         self.rules[name] = Rule(name=name, text=text)


@dataclass
class Turn(deque, DataClassJsonMixin):
    """Turn is a deque-like object for save
    sata about game turns

    Args:
        name (str): name of Turn.
        _order (List[Rule]): list of default elements of Turn.
    """
    name: str
    _order: List[Rule] = field(
        default_factory=list,
        repr=False,
        metadata=config(exclude=lambda x: True),
        )

    def add_phase(self, name: str, text: str):
        """Add rule to basic structure of turn
        Yhis structure is a list of Rules. The method
        new_cycle() instantiaate the turn inside
        Turn class.

        Args:
            name (str): name of phase rule
            text (str): text of phase rule
        """
        self._order.append(Rule(name=name, text=text))

    def new_cycle(self):
        """Clear the Turn and instantiate new turn
        """
        self.clear()
        self.extend(self._order)

    def __repr__(self):
        items = (f"{rule.name}={rule.text}" for rule in self)
        return "{}({})".format(self.__class__.__name__, ", ".join(items))


RULES = {
    # 'rule': Rule,
    'turn': Turn,
    }
RULES_TYPES = Literal['turn']
