from CS235Flix.domain.model import WatchList, Movie

import pytest

@pytest.fixture()
def watchlist():
    return WatchList()

def test_cr3(watchlist):
    watchlist = WatchList()
    print(f"Size of watchlist: {watchlist.size()}")
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Ice Age", 2002))
    watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))
    print(watchlist.first_movie_in_watchlist())
    print(watchlist.size())
    watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))
    print(watchlist.size())
    watchlist.remove_movie(Movie("Moana", 2016))
    print(watchlist.size())
    watchlist.remove_movie(Movie("Moana", 2016))
    print(watchlist.size())
    print(watchlist.select_movie_to_watch(1))
    print(watchlist.select_movie_to_watch(100))
    watchlist.add_movie(Movie("Yasuo The Retarded", 2012))
    i = iter(watchlist)
    for movie in i:
        print(movie)

