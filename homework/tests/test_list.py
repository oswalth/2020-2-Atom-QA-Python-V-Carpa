import pytest


extend_parameters = [
    'init_list, obj_to_extend, expected_list',
    [
        ([1, 2, 3], [4], [1, 2, 3, 4]),
        ([1, 2, 3], (4,), [1, 2, 3, 4]),
        ([1, 2, 3], {4: 'd'}, [1, 2, 3, 4]),
        ([1, 2, 3], set([4, 4, 5]), [1, 2, 3, 4, 5]),
    ]
]


class TestList:

    @pytest.mark.parametrize(*extend_parameters)
    def test_extend(self, init_list, obj_to_extend, expected_list):
        init_list.extend(obj_to_extend)
        assert init_list == expected_list

    def test_add(self):
        assert [1, 2, 3] + [4] == [1, 2, 3, 4]

    def test_append_list(self):
        init_list = [1, 2, 3]
        init_list.append([4])
        assert init_list == [1, 2, 3, [4]]

    def test_pop(self):
        init_list = [1, 2, 3]
        assert (init_list.pop(0), init_list) == (1, [2, 3])

    def test_multiply(self):
        init_list = [1, 2, 3]
        assert init_list * 2 == [1, 2, 3, 1, 2, 3]
