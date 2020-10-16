import pytest


add_parameters = [
    'init_set, val_to_add, expected_set',
    [
        ({1, 2, 3}, 4, {1, 2, 3, 4}),
        ({1, 2, 3}, '4', {1, 2, 3, '4'}),
        ({1, 2, 3}, (4, 5), {1, 2, 3, (4, 5)}),
        ({1, 2, 3}, 3, {1, 2, 3})
    ]
]


class TestSet:

    @pytest.mark.parametrize(*add_parameters)
    def test_add(self, init_set, val_to_add, expected_set):
        init_set.add(val_to_add)
        assert init_set == expected_set

    def test_difference(self):
        x = {"apple", "banana", "cherry"}
        y = {"google", "microsoft", "apple"}
        assert x.difference(y) == {'banana', 'cherry'}

    def test_intersection(self):
        x = {"apple", "banana", "cherry"}
        y = {"google", "microsoft", "apple"}
        assert x.intersection(y) == {"apple"}

    def test_issubset(self):
        x = {"a", "b", "c"}
        y = {"f", "e", "d", "c", "b", "a"}
        assert x.issubset(y)

    def test_clear(self):
        set_ = {1, 2, 3}
        set_.clear()
        assert set_ == set()
