import pytest


extend_parameters = [
    'dict_, obj_to_find, method',
    [
        ({1: 'a', 2: 'b'}, 1, 'keys'),
        ({1: 'a', 2: 'b'}, (1, 'a'), 'items'),
        ({1: 'a', 2: 'b'}, 'b', 'values'),
    ]
]


class TestDict:

    @pytest.mark.parametrize(*extend_parameters)
    def test_in(self, dict_, obj_to_find, method):
        assert obj_to_find in getattr(dict_, method)()

    def test_assign(self):
        dict_ = {1: 'a', 2: 'b'}
        dict_[3] = 'c'
        assert dict_ == {1: 'a', 2: 'b', 3: 'c'}

    def test_reassign(self):
        dict_ = {1: 'a', 2: 'b'}
        dict_[2] = 'c'
        assert dict_ == {1: 'a', 2: 'c'}

    def test_pop(self):
        dict_ = {1: 'a', 2: 'b'}
        dict_.pop(1)
        assert dict_ == {2: 'b'}

    def test_clear(self):
        dict_ = {1: 'a', 2: 'b'}
        dict_.clear()
        assert dict_ == dict()
