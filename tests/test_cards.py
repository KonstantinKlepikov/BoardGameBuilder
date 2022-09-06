import pytest, json
from bgameb.cards import Card, CardTexts


class TestCardText:
    """Test CardText class
    """

    def test_card_text_operations(self) -> None:
        """Test get, set and delete operations of
        CardText
        """
        text = CardTexts()
        text.this = 'this'
        assert text.this == 'this', 'not set or cant get'
        assert text.__repr__() == "CardTexts(this='this')", 'wrong repr'
        text.this = 'that'
        assert text.this == 'that', 'not set or cant update'
        del text.this
        with pytest.raises(
            AttributeError, match='this'
            ):
            text.this
        with pytest.raises(
            KeyError, match='this'
            ):
            del text.this

    def test_card_text_equal(self) -> None:
        """Test equal of CardTexts
        """
        text1 = CardTexts()
        text2 = CardTexts()
        assert text1 == text2, 'not equal'
        text2.this = 'this'
        assert text1 != text2, 'equal'


class TestCard:
    """Test Card class"""

    def test_card_instanciation(self) -> None:
        """Test card correct created
        """
        card = Card()
        assert card.name == 'card', 'wrong name'
        assert card.open == False, 'card is open'
        assert card.tapped == False, 'card is tapped'
        assert card.side == None, 'defined wrong side'
        assert isinstance(card.text, CardTexts), 'texts not seted'

    def test_card_class_is_converted_to_json(self) -> None:
        """Test to json convertatrion
        """
        card = Card()
        j = json.loads(card.to_json())
        assert j['name'] == 'card', 'not converted to json'

    def test_card_texts(self) -> None:
        """Test card text can be set, get, delete
        """
        card = Card()
        card.text.this = 'this'
        assert card.text.this == 'this', 'not set or cant get'
        del card.text.this
        with pytest.raises(
            AttributeError, match='this'
            ):
            card.text.this

    def test_flip(self) -> None:
        """Test flip card
        """
        card = Card()
        card.flip()
        assert card.open, 'card not oppened'
        card.flip()
        assert not card.open, 'card oppened'

    def test_fase_up(self) -> None:
        """Test face up open card and return text
        """
        card = Card()
        texts = card.face_up()
        assert card.open, 'card not open'
        assert isinstance(texts, CardTexts), 'wrong text'

    def test_fase_down(self) -> None:
        """Test face up hide card
        """
        card = Card()
        card.open = True
        card.face_down()
        assert not card.open, 'card not open'

    def test_tap_tap_card_and_set_side(self) -> None:
        """Test tap card tap and set side
        """
        card = Card()
        card.tap(side='left')
        assert card.tapped, 'card not tapped'
        assert card.side == 'left', 'wrong side'

    def test_untap_card(self) -> None:
        """Test tap card tap and set side
        """
        card = Card()
        card.tapped = True
        assert card.tapped, 'card not tapped'
        card.untap()
        assert not card.tapped, 'card not untapped'
