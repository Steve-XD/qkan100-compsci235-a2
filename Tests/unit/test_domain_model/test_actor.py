from CS235Flix.domain.model import Actor
import pytest

@pytest.fixture()
def actor():
    return Actor('')

def test_init(actor):
    actor1 = Actor("Angelina Jolie")
    assert repr(actor1) == "<Actor Angelina Jolie>"
    actor2 = Actor("")
    assert actor2.actor_full_name is None
    actor3 = Actor(42)
    assert actor3.actor_full_name is None
    # check for equality of two Director object instances by comparing the names
    actor4 = Actor("Angelina Jolie")
    assert (actor1 == actor4) == True
    # implement a sorting order defined by the name
    a_list = []
    actor5 = Actor("Aatrox")
    a_list.append(actor1)
    a_list.append(actor5)
    a_list.sort()
    assert a_list[0] == actor5
    # defines which attribute is used for computing a hash value as used in set or dictionary keys
    actors = {actor1, actor4}
    assert len(actors) == 1
    # add coleague and check whether it is inside the list
    actor1.add_actor_colleague(actor5)
    assert actor1.check_if_this_actor_worked_with(actor5) == True

