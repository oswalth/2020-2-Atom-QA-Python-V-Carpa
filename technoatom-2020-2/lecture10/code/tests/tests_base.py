import pytest


@pytest.fixture()
def prepare():
    print('data was prepared')


def test_1_negative(prepare):
    assert 5 + 2 == 8


def test_2_positive(prepare):
    assert 6 // 2 == 3


def test_3_negative(prepare):
    assert '\\' + '123' == '\\1234'


def test_4_positive(prepare):
    assert '25' * 3 == '252525'