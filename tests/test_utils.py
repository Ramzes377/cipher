from src.utils import apply_recursive


def test_apply_recursive():
    data = {'1': ['nested-data', 'another-data'], '2': ['kek']}

    r = apply_recursive(lambda v: v + '7', data)
    expected = {'17': ['nested-data7', 'another-data7'], '27': ['kek7']}
    assert r == expected
