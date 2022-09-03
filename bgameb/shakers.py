"""Game shakers - dice towers, bags and etc
"""
from typing import Dict, Tuple, TypeVar, List, Union
from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin
from bgameb.rollers import BaseRoller


RollerCls = TypeVar('RollerCls', bound=BaseRoller)
ShakerRollers = Dict[str, Dict[str, Union[RollerCls, int]]]
ShakerResult = Dict[str, Dict[str, Tuple[int]]]


@dataclass
class Shaker(DataClassJsonMixin):
    """Create shaker for roll dices or flip coins
    """
    name: str = 'shaker'
    rollers: ShakerRollers = field(default_factory=dict, init=False) #TODO: use namedtuple or dataclass
    last_roll: ShakerResult = field(default_factory=dict, init=False) #TODO: use namedtuple or dataclass

    def __post_init__(self):
        self.rollers = {}
        self.last_roll = {}

    def add(self, roller: RollerCls, color: str = 'white', count: int = 1) -> None:
        """Add roller to shaker

        Args:
            roller (RollerCls):roller class instance
            color (str, optional): color groupe. Defaults to 'white'.
            count (int, optional): count of rollers copy. Defaults to 1.

        Raises:
            RollerDefineError: counts not set or are different rollers with same names
        """
        if count < 1:
            raise RollerDefineError('Need at least one roller')
        if self.rollers.get(color):
            if roller.name not in self.rollers[color].keys():
                self.rollers[color][roller.name] = {'roller': roller, 'count': count}
            elif self.rollers[color][roller.name]['roller'] is not roller:
                raise RollerDefineError(
                    f'Different instances of roller class with same name {roller.name}'
                    )
            else:
                self.rollers[color][roller.name]['count'] += count
        else:
            self.rollers[color] = {roller.name: {'roller': roller, 'count': count}}

    def remove(self, name: str, count: int, color: str) -> None:
        """Remove any kind of roller copy from shaker by name and color

        Args:
            name (str): name of roller
            count (int): count of rollers to delete
            color (str): color froup of rollers

        Raises:
            RollerDefineError: name, color not match or count of rollers not defined
        """
        if count < 1:
            raise RollerDefineError('Need at least one roller')
        if self.rollers.get(color):
            if self.rollers[color].get(name):
                if self.rollers[color][name]['count'] <= count:
                    del self.rollers[color][name]
                    if len(self.rollers[color]) == 0:
                        del self.rollers[color]
                else:
                    self.rollers[color][name]['count'] -= count
            else:
                raise RollerDefineError(
                    f'Cant find roller with name {name}'
                    )
        else:
            raise RollerDefineError(
                f'Cant find roller with collor {color}'
                )

    def remove_all_by_color(self, color: str) -> None:
        """Remove all rollers by color from shaker.
        If no any color is match, nothing happens.

        Args:
            name (str): name of roller
        """
        if color in self.rollers.keys():
            del self.rollers[color]

    def remove_all_by_name(self, name: str) -> None:
        """Remove all rollers by roller name from shaker.
        If no any name is match, nothing happens.

        Args:
            name (str): name of roller
        """
        to_del = []
        for color in self.rollers.keys():
            self.rollers[color].pop(name, None)
            if len(self.rollers[color]) == 0:
                to_del.append(color)
        if to_del:
            self._remove_empty_colors(to_del)

    def remove_all(self) -> None:
        """Remove all rollers from shaker
        """
        self.rollers = {}

    def _remove_empty_colors(self, to_del: List[str]) -> None:
        """Remove empty colors items from rollers dict

        Args:
            to_del (List[str]): list of colors
        """
        for color in to_del:
            del self.rollers[color]

    def roll(self) -> ShakerResult:
        """Roll all rollers with shaker and return results

        Return:
            Dict[str, Dict[str, Tuple[int]]]: result of roll

        .. code-block::
            :caption: Example:

                {"white": {"six_dice": (5, 3, 2, 5)}}
        """
        roll = {}
        for color, rollers in self.rollers.items():
            roll[color] = {}
            for name, obj in rollers.items():
                roll[color][name] = tuple(
                    obj['roller'].roll() for _ in range(obj['count'])
                    )
        if roll:
            self.last_roll = roll
            return self.last_roll
        else:
            return {}


class RollerDefineError(AttributeError):
    """Count of rollers not defined
    """
    pass
