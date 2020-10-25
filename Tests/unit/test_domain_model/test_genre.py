from CS235Flix.domain.model import Genre
import pytest

@pytest.fixture()
def genre():
    return Genre("")

def test_init(genre):
    genre1 = Genre("Horror")
    assert repr(genre1) == "<Genre Horror>"
    genre2 = Genre("")
    assert genre2.genre_name is None
    genre3 = Genre(42)
    assert genre3.genre_name is None
    # check for equality of two Director object instances by comparing the names
    genre4 = Genre("Horror")
    assert (genre1 == genre4) == True
    # implement a sorting order defined by the name
    a_list = []
    genre5 = Genre("History")
    a_list.append(genre1)
    a_list.append(genre5)
    a_list.sort()
    assert a_list[0] == genre5
    # defines which attribute is used for computing a hash value as used in set or dictionary keys
    genre_set = {genre1, genre4}
    assert len(genre_set) == 1

