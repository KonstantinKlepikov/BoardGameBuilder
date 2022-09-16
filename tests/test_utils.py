import pytest
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from bgameb.utils import get_random_name, fill_dataclass


@pytest.mark.slow
def test_get_random_name() -> None:
    """get_random_name() returns random words
    """
    words = set()
    for i in range(100):
        w = get_random_name()
        print(w)
        assert 6 <= len(w) <= 10, 'wrong len of words'
        words.add(w)
    assert len(words) == 100, 'not a random'


def test_fill_dataclass() -> None:
    """fill_dataclass() correct fill datacalass from another
    """
    @dataclass_json
    @dataclass
    class This:
        name: str

    @dataclass_json
    @dataclass
    class That:
        name: str

    this = This(name='some_name')
    that = fill_dataclass(this, That)
    assert isinstance(that, That), 'not an instance'
    assert that.name == 'some_name', 'is wrong name'

    class This:
        def __init__(self, name):
            self.name = name

    this = This(name='some_name')
    with pytest.raises(
        ValueError,
        match='is not a dataclass!'
        ):
        fill_dataclass(this, That)
