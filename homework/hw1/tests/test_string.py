import pytest


extend_parameters = [
    'separator, obj_to_join, expected_string',
    [
        (' separator ', '123', '1 separator 2 separator 3'),
        (', ', ['1', '2', '3'], '1, 2, 3'),
        ('\t', {'1': 1, '2': 2, '3': 3}, '1\t2\t3')
    ]
]

encode_parameters = [
    'init_string, encoding, expected_string',
    [
        ('a', 'utf-8', b'a'),
        ('a', 'utf-16', b'\xff\xfea\x00'),
        ('a', 'cp1251', b'a')
    ]
]


class TestString:

    @pytest.mark.parametrize(*encode_parameters)
    def test_encode(self, init_string, encoding, expected_string):
        assert init_string.encode(encoding) == expected_string

    @pytest.mark.parametrize(*extend_parameters)
    def test_join(self, separator, obj_to_join, expected_string):
        assert separator.join(obj_to_join) == expected_string

    def test_add(self):
        init_string = 'abc'
        assert init_string + 'd' == 'abcd'

    def test_multiply(self):
        assert 'abc' * 2 == 'abcabc'

    def test_isalpha(self):
        assert 'abc'.isalpha() == True
