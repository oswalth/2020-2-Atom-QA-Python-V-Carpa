import pytest


sum_parameters = [
    'value1, value2, result',
    [
        (1, 2, 3),
        (0.1, 0.2, 0.3)
    ]
]

division_parameters = [
    'value1, value2, result',
    [
        (1, 0.5, 2.0),
        (2, 1, 2),
        (2, 1, 2.0)
    ]
]

power_parameters = [
    'value1, value2, result',
    [
        (2, 2, 4),
        (4, 1 / 2, 2.0),
        (4, -1, 1 / 4)
    ]
]


class TestInt:

    @pytest.mark.parametrize(*sum_parameters)
    def test_sum(self, value1, value2, result):
        assert value1 + value2 == result

    @pytest.mark.parametrize(*division_parameters)
    def test_division(self, value1, value2, result):
        assert value1 / value2 == result

    def test_e_notation(self):
        assert 1e3 == 1000

    def test_power(self, value1, value2, result):
        assert value1 ** value2 == result

    def test_single_entity(self):
        a = 20
        b = 20
        assert a is b
