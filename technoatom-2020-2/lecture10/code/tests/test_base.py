import pytest


@pytest.fixture(autouse=True)
def prepare():
    print('run prepare')


def test_positive():
    assert 4 // 2 == 2


def test2_positive():
    assert 3 * 4 == 12


def test3_positive():
    assert '*' * 3 == '***'