from CS235Flix.domain.model import Movie, Genre, Actor, Director

import pytest

@pytest.fixture()
def movie():
    return Movie('', 0)

def test_init(movie):
    #test cr3
    movie1 = Movie("Moana", 2016)
    assert repr(movie1) == "<Movie Moana, 2016>"
    movie3 = Movie("Moana", 1899)
    assert movie3.title is None
    # check for equality of two Director object instances by comparing the names
    movie4 = Movie("Moana", 2016)
    assert (movie1 == movie4) == True
    # implement a sorting order defined by the name
    a_list = []
    movie5 = Movie("Yasuo The Retarded", 2015)
    a_list.append(movie5)
    a_list.append(movie1)
    a_list.sort()
    assert a_list[0] == movie1
    # defines which attribute is used for computing a hash value as used in set or dictionary keys
    movies = {movie1, movie4}
    assert len(movies) == 1
    movie5 = Movie("Moana", 2015)
    movies = {movie1, movie5}
    assert len(movies) == 2

def test_properties(movie):
    movie1 = Movie("Moana", 2016)
    movie1.title = "Hokage" # legal title
    assert repr(movie1) == "<Movie Hokage, 2016>"
    movie1.title = 1234  # illegal title
    assert repr(movie1) == "<Movie Hokage, 2016>"

    movie2 = Movie("Raikage", 2004)
    movie2.description = " Faster than speed of light for real "  # legal description
    assert movie2.description == "Faster than speed of light for real"
    movie2.description = ""  # illegal description
    assert movie2.description == "Faster than speed of light for real"

    movie3 = Movie("Moana", 2016)
    actor = Actor("Jacinda Adern")
    director = Director("Ron Clements")
    movie3.director = actor #illegal director
    assert movie3.director is None
    movie3.director = director #legal director
    assert repr(movie3.director) == "<Director Ron Clements>"

    actors = [Actor("Auli'i Cravalho"), Actor("Dwayne Johnson"), Actor("Rachel House"), Actor("Temuera Morrison")]
    for actor in actors:
        movie3.add_actor(actor) ##legal adding actor
    assert str(movie3.actors) == "[<Actor Auli'i Cravalho>, <Actor Dwayne Johnson>, <Actor Rachel House>, <Actor Temuera Morrison>]"
    movie3.add_actor(director) ##illegal adding actor
    assert str(movie3.actors) == "[<Actor Auli'i Cravalho>, <Actor Dwayne Johnson>, <Actor Rachel House>, <Actor Temuera Morrison>]"
    movie3.remove_actor(Actor("Rachel House")) ##legal remove actor
    assert str(movie3.actors) == "[<Actor Auli'i Cravalho>, <Actor Dwayne Johnson>, <Actor Temuera Morrison>]"
    movie3.remove_actor(director)  ##illegal remove actor
    assert str(movie3.actors) == "[<Actor Auli'i Cravalho>, <Actor Dwayne Johnson>, <Actor Temuera Morrison>]"
    movie3.actors = Actor("Dwayne Johnson") ##test setter
    assert str(movie3.actors) == "[<Actor Dwayne Johnson>]"

    genres = [Genre("Comedy"), Genre("Action"), Genre("Disney"), Genre("Romantic")]
    for genre in genres:
        movie3.add_genre(genre)  ##legal adding genre
    assert str(sorted(movie3.genres)) == "[<Genre Action>, <Genre Comedy>, <Genre Disney>, <Genre Romantic>]"
    movie3.add_genre(director)  ##illegal adding genre
    assert str(movie3.genres) == "[<Genre Comedy>, <Genre Action>, <Genre Disney>, <Genre Romantic>]"
    movie3.remove_genre(Genre("Romantic"))  ##legal remove genre
    assert str(movie3.genres) == "[<Genre Comedy>, <Genre Action>, <Genre Disney>]"
    movie3.remove_genre(director)  ##illegal remove genre
    assert str(movie3.genres) == "[<Genre Comedy>, <Genre Action>, <Genre Disney>]"
    movie3.genres = Genre("Comedy") ##test setter
    assert str(movie3.genres) == "[<Genre Comedy>]"

    movie3.runtime_minutes = 107 ## legal runtime
    assert "Movie runtime: {} minutes".format(movie3.runtime_minutes) == "Movie runtime: 107 minutes"
    with pytest.raises(ValueError):
        movie3.runtime_minutes = -1 ## illegal runtime

    ###################################### test extension ######################################

    movie3.rank = 185  ## legal rank
    assert movie3.rank == 185
    with pytest.raises(ValueError):
        movie3.rank = -1  ## illegal rank

    movie3.rating = 8.1  ## legal rating
    assert movie3.rating == 8.1
    with pytest.raises(ValueError):
        movie3.rating = 11  ## illegal rating

    movie3.votes = 107583  ## legal votes
    assert movie3.votes == 107583
    with pytest.raises(ValueError):
        movie3.votes = -1  ## illegal votes

    movie3.revenue_millions = 510.365  ## legal revenue_millions
    assert movie3.revenue_millions == 510.365
    with pytest.raises(ValueError):
        movie3.revenue_millions = -510.365  ## illegal revenue_millions

    movie3.metascore = 91.6  ## legal metascore
    assert movie3.metascore == 91.6
    with pytest.raises(ValueError):
        movie3.metascore = -91.6  ## illegal metascore



