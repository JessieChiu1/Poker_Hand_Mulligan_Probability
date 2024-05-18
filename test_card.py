from card import Card

def test_card():
    # Test initialization
    card = Card("♥️", 2)
    assert card.suit == "♥️"
    assert card.value == 2
    assert card.face == "2"

    # Test get_face_name()
    assert card.get_face_name() == "2"

    # Test __str__()
    assert str(card) == "2♥️"

# Test non-numbered card
def test_ace_card():
    # Test Ace card
    ace_card = Card("♠️", 14)
    assert ace_card.suit == "♠️"
    assert ace_card.value == 14
    assert ace_card.face == "Ace"

    assert ace_card.get_face_name() == "Ace"

    assert str(ace_card) == "Ace♠️"