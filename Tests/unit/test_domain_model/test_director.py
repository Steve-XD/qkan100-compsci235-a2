from CS235Flix.domain.model import Director
import pytest

@pytest.fixture()
def director():
    return Director('')

def test_init(director):
    director1 = Director("Taika Waititi")
    assert repr(director1) == "<Director Taika Waititi>"
    director2 = Director("")
    assert director2.director_full_name is None
    director3 = Director(42)
    assert director3.director_full_name is None
    # check for equality of two Director object instances by comparing the names
    director4 = Director("Taika Waititi")
    assert (director1 == director4) == True
    # implement a sorting order defined by the name
    a_list = []
    director5 = Director("Alex")
    a_list.append(director1)
    a_list.append(director5)
    a_list.sort()
    assert a_list[0] == director5
    # defines which attribute is used for computing a hash value as used in set or dictionary keys
    directors = {director1, director4}
    assert len(directors) == 1

