import pytest
from bgameb.utils import get_random_name


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
