from core.models import Item, new_id


def test_item_round_trips_through_dict():
    item = Item(id="abc123", name="Oscilloscope", note="Bench 4")
    restored = Item.from_dict(item.to_dict())
    assert restored == item


def test_to_dict_returns_only_strings():
    item = Item(id="abc123", name="Oscilloscope", note="Bench 4")
    assert all(isinstance(v, str) for v in item.to_dict().values())


def test_new_id_is_unique():
    assert new_id() != new_id()


def test_new_id_is_short_and_printable():
    value = new_id()
    assert len(value) == 8
    assert value.isalnum()
