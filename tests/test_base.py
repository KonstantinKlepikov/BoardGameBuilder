import pytest
from bgameb.base import Components
from bgameb.stuff import Dice, Card, BaseStuff
from bgameb.errors import ComponentNameError


class TestComponents:
    """Test CardText class
    """
    components = [
        (Dice, 'dice'),
        (Card, 'card'),
        ]

    @pytest.mark.parametrize("_class, name", components)
    def test_components_access_to_attr(self, _class, name: str) -> None:
        """Test components acces to attrs
        """
        comp = Components()
        comp.__dict__.update(
            {'some': _class(name=name), 'many': _class(name=name)}
            )

        assert comp.some.name == name, 'not set or cant get'
        assert comp['some'].name == name, 'not set or cant get'

        comp.this = _class(name=name)
        assert comp.this.name == name, 'not setted attr'
        comp['that'] = _class(name=name)
        assert comp.that.name == name, 'not setted attr'

        del comp.some
        with pytest.raises(AttributeError, match='some'):
            comp.some
        with pytest.raises(KeyError, match='some'):
            comp['some']

        with pytest.raises(AttributeError, match='newer'):
            del comp.newer
        with pytest.raises(KeyError, match='newer'):
            del comp['newer']

    @pytest.mark.parametrize("_class, name", components)
    def test_components_repr(self, _class, name: str) -> None:
        """Test components repr
        """
        comp = Components()
        comp.__dict__.update({'some': _class(name=name)})
        assert "Components(some=" in comp.__repr__(), 'wrong repr'

    @pytest.mark.parametrize("_class, name", components)
    def test_components_len(self, _class, name: str) -> None:
        """Test components len
        """
        comp1 = Components()
        comp2 = Components()
        comp1.__dict__.update({'some': _class(name=name)})
        assert len(comp1) == 1, 'wrong len'
        assert len(comp2) == 0, 'wrong len'

    @pytest.mark.parametrize("_class, name", components)
    def test_components_items(self, _class, name: str) -> None:
        """Test components items access
        """
        comp = Components()
        comp.__dict__.update({'some': _class(name=name)})
        assert len(comp.items()) == 1, 'items not accessed'
        assert len(comp.keys()) == 1, 'keys not accessed'
        assert len(comp.values()) == 1, 'values not accessed'

    @pytest.mark.parametrize("_class, name", components)
    def test_update_component(self, _class, name: str) -> None:
        """Test update component
        """
        comp = Components()
        comp._update(_class, {'name': name})
        comp[name].name == name, 'wrong name'
        with pytest.raises(
            ComponentNameError,
            match='Component with name'
        ):
            comp._update(_class, {'name': None})

    @pytest.mark.parametrize("_class, name", components)
    def test_add_component(self, _class, name: str) -> None:
        """Test add component with add() method
        """
        comp = Components()
        comp._add(_class, name=name)
        assert comp[name], 'component not added'
        with pytest.raises(
            ComponentNameError,
            match='is exist in'
        ):
            comp._add(_class, name=name)
        comp._add(Dice, name='this_is')
        assert comp.this_is, 'component not added'
        with pytest.raises(
            ComponentNameError,
            match='is exist in'
        ):
            comp._add(_class, name='this_is')
        if isinstance(_class, BaseStuff):
            comp._add(_class, name='this_is_five', sides=5)
            assert comp.this_is_five.sides == 5, 'component not added'

    @pytest.mark.parametrize("_class, name", components)
    def test_add_replace_component(self, _class, name: str) -> None:
        """Test add_replace() method
        """
        comp = Components()
        comp._add_replace(_class, name=name)
        add1 = id(comp[name])
        assert comp[name], 'component not added'
        comp._add_replace(_class, name=name)
        assert id(comp[name]) != add1, 'not replaced'
        comp._add_replace(_class, name='this_is')
        assert comp.this_is, 'component not added'
        if isinstance(_class, BaseStuff):
            comp._add_replace(_class, name='this_is_five', sides=5)
            assert comp.this_is_five.sides == 5, 'component not added'

    @pytest.mark.parametrize("_class, name", components)
    def test_get_names(self, _class, name: str) -> None:
        """Test get_names() method
        """
        comp = Components()
        assert comp.get_names() == [], 'nonempty list of names'
        comp._add(_class, name=name)
        assert comp.get_names() == [name], 'empty list of names'
        comp._add(_class, name='this')
        assert comp.get_names() == [name, 'this'], 'empty list of names'
