from dotick.items.models import Item
from dotick.organization.models import Column, Folder, List


def _index_fields(model):
    return {tuple(index.fields) for index in model._meta.indexes}


def test_increment_one_query_indexes_cover_organization_and_item_access_paths():
    assert ("owner", "position") in _index_fields(Folder)
    assert ("folder", "position") in _index_fields(List)
    assert ("list", "position") in _index_fields(Column)
    assert ("owner", "is_trashed", "-updated_at") in _index_fields(Item)
    assert ("column", "is_trashed", "-updated_at") in _index_fields(Item)
    assert ("owner", "kind", "is_trashed") in _index_fields(Item)
