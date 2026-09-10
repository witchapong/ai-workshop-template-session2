import pytest

from core.storage import load, save, append


def test_load_returns_empty_list_when_file_missing(tmp_path):
    assert load("nothing", data_dir=tmp_path) == []


def test_save_then_load_round_trips(tmp_path):
    records = [
        {"id": "1", "name": "Scope", "note": "Bench 4"},
        {"id": "2", "name": "Meter", "note": "Bench 1"},
    ]
    save("kit", records, data_dir=tmp_path)
    assert load("kit", data_dir=tmp_path) == records


def test_append_adds_to_existing_file(tmp_path):
    save("kit", [{"id": "1", "name": "Scope"}], data_dir=tmp_path)
    append("kit", {"id": "2", "name": "Meter"}, data_dir=tmp_path)
    assert load("kit", data_dir=tmp_path) == [
        {"id": "1", "name": "Scope"},
        {"id": "2", "name": "Meter"},
    ]


def test_append_creates_file_when_missing(tmp_path):
    append("fresh", {"id": "1", "name": "Scope"}, data_dir=tmp_path)
    assert load("fresh", data_dir=tmp_path) == [{"id": "1", "name": "Scope"}]


def test_save_empty_list_produces_empty_load(tmp_path):
    save("kit", [], data_dir=tmp_path)
    assert load("kit", data_dir=tmp_path) == []


def test_append_rejects_record_with_different_columns(tmp_path):
    save("kit", [{"id": "1", "name": "Scope"}], data_dir=tmp_path)
    with pytest.raises(ValueError, match="columns"):
        append("kit", {"id": "2", "colour": "blue"}, data_dir=tmp_path)
