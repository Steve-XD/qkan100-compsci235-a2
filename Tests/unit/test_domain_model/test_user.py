from CS235Flix.domain.model import Movie, Review, User
import datetime
import pytest

@pytest.fixture()
def user():
    return User("","")

def test_init(user):
    #test cr3
    user1 = User('Martin', 'pw12345')
    user2 = User('Ian', 'pw67890')
    user3 = User('Daniel', 'pw87465')
    assert repr(user1) == "<User Martin pw12345>"
    assert repr(user2) == "<User Ian pw67890>"
    assert repr(user3) == "<User Daniel pw87465>"

    #test username
    assert user1.username == "Martin"
    user1.username = 900 ##illegal
    assert user1.username == "Martin"
    user1.username = " STEVEN " ##legal
    assert user1.username == "STEVEN"

    #test password
    assert user1.password == 'pw12345'
    user1.password = 900  ##illegal
    assert user1.password == 'pw12345'
    user1.password = "pv wej asd 123" ##legal
    assert user1.password == "pv wej asd 123"

    #test watched_movie
    timestamp = datetime.date
    movie1 = Movie("Moana", 2016)
    movie1.runtime_minutes = 178
    movie2 = Movie("My life is a Legend!", 1905)
    movie2.runtime_minutes = 2000
    user1.watch_movie(movie1) ##legal
    user1.watch_movie(movie2)
    assert str(user1.watched_movies) == "[<Movie Moana, 2016>, <Movie My life is a Legend!, 1905>]"
    review1 = Review(user1, movie1, "Fantastic movie", timestamp, 9 )
    user1.watch_movie(review1) ##illegal
    assert str(user1.watched_movies) == "[<Movie Moana, 2016>, <Movie My life is a Legend!, 1905>]"
    user1.watched_movies = movie1
    assert str(user1.watched_movies) == "[<Movie Moana, 2016>]"
    user1.watched_movies = review1
    assert str(user1.watched_movies) == "[<Movie Moana, 2016>]"

    # test reviews
    review2 = Review(user1, movie2, "Horrible movie",  timestamp, 3 )
    user1.add_review(review1) ##legal
    user1.add_review(review2)
    assert str(user1.reviews) == "[<Review (9/10):Fantastic movie>, <Review (3/10):Horrible movie>]"
    user1.add_review(movie1) ##illegal
    assert str(user1.reviews) == "[<Review (9/10):Fantastic movie>, <Review (3/10):Horrible movie>]"
    user1.reviews = review1 ##legal
    assert str(user1.reviews) == "[<Review (9/10):Fantastic movie>]"
    user1.reviews = movie2 ##illegal
    assert str(user1.reviews) == "[<Review (9/10):Fantastic movie>]"

    # test time_spent_watching_movies_minutes
    assert user1.time_spent_watching_movies_minutes == 2178
    user1.time_spent_watching_movies_minutes = 2000  #LEGAL
    assert user1.time_spent_watching_movies_minutes == 2000
    user1.time_spent_watching_movies_minutes = -1 #illegal
    assert user1.time_spent_watching_movies_minutes == 2000

    ## test __eq__
    user4 = User('SteVen', 'pv wej asd 123')
    assert user1 == user4

    ## test __lt__
    a_list = [user1, user2, user3]
    assert str(a_list) == "[<User STEVEN pv wej asd 123>, <User Ian pw67890>, <User Daniel pw87465>]"
    a_list.sort()
    assert str(a_list) == "[<User Daniel pw87465>, <User Ian pw67890>, <User STEVEN pv wej asd 123>]"

    ## test __hash__
    assert len({user1, user4}) == 1





