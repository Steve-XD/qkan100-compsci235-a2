from datetime import date

import pytest

from CS235Flix.authentication.services import AuthenticationException
from CS235Flix.authentication import services as auth_services
from CS235Flix.movies import services as movies_services
from CS235Flix.movies.services import NonExistentMovieException
from CS235Flix.domain.model import Actor, Director, Genre, Movie, Review, User, WatchList, make_review


def test_can_add_user(in_memory_repo):
    new_username = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_username, in_memory_repo)
    assert user_as_dict['username'] == new_username

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    username = 'thorke'
    password = 'abcd1A23'

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(username, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_username, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_username, '0987654321', in_memory_repo)

def test_can_add_comment(in_memory_repo):
    comment_text = 'The loonies are stripping the supermarkets bare!'
    username = 'fmercury'

    # Call the service layer to add the comment.
    movies_services.add_review(10,2,comment_text, username, in_memory_repo)

    # Retrieve the reviews for the article from the repository.
    reviews_as_list = movies_services.get_reviews(2, in_memory_repo)

    # Check that the comments include a comment with the new comment text.
    assert str(reviews_as_list) == "[<Review (10/10):The loonies are stripping the supermarkets bare!>]"


def test_cannot_add_comment_for_non_existent_article(in_memory_repo):
    rank = 1001
    comment_text = "COVID-19 - what's that?"
    username = 'fmercury'

    # Call the service layer to attempt to add the comment.
    with pytest.raises(movies_services.NonExistentMovieException):
        movies_services.add_review(10,rank,comment_text, username, in_memory_repo)


def test_cannot_add_comment_by_unknown_user(in_memory_repo):
    rank = 2
    comment_text = "COVID-19 - what's that?"
    username = 'gmichael'

    # Call the service layer to attempt to add the comment.
    with pytest.raises(movies_services.UnknownUserException):
        movies_services.add_review(10,rank,comment_text, username, in_memory_repo)


def test_can_get_first_11_movie(in_memory_repo):
    movie_list = movies_services.get_11_movie(in_memory_repo)
    assert len(movie_list)==11

def test_can_get_random_movies(in_memory_repo):
    movie_list = movies_services.get_10_movie('random',in_memory_repo)
    assert len(movie_list)==10

def test_can_get_random_movies_based_on_genres(in_memory_repo):
    genre1 = Genre('Fantasy')
    genre2 = Genre('Action')
    genre3 = Genre('Drama')
    genre4 = Genre('Music')
    movie_list = movies_services.get_10_movie([genre1], in_memory_repo)
    assert len(movie_list) == 10
    movie_list = movies_services.get_10_movie([genre1, genre2], in_memory_repo)
    assert len(movie_list) == 10
    movie_list = movies_services.get_10_movie([genre1, genre2, genre3], in_memory_repo)
    assert len(movie_list) == 10
    movie_list = movies_services.get_10_movie([genre1, genre2, genre3, genre4], in_memory_repo)
    assert len(movie_list) == 10

def test_can_get_movie_by_rank(in_memory_repo):
    rank = 1
    movie_obj = movies_services.get_movie(rank,in_memory_repo)
    assert movie_obj.rank == rank

def test_can_get_review_by_rank(in_memory_repo):
    rank = 1
    review_list = movies_services.get_reviews(rank,in_memory_repo)
    assert len(review_list) == 3

def test_can_get_movies_by_year_and_genre(in_memory_repo):
    movie_list = movies_services.get_all_movie(['All','All'],in_memory_repo)
    assert len(movie_list) == 1000
    movie_list = movies_services.get_all_movie(["Fantasy", 'All'], in_memory_repo)
    assert len(movie_list) == 101
    movie_list = movies_services.get_all_movie(["All", '2016'], in_memory_repo)
    assert len(movie_list) == 297
    movie_list = movies_services.get_all_movie(["Fantasy", '2016'], in_memory_repo)
    assert len(movie_list) == 23
    movie_list = movies_services.get_all_movie(["Western", '2009'], in_memory_repo)
    assert str(movie_list) == 'None'

def test_can_get_all_genres(in_memory_repo):
    genre_list = movies_services.get_all_genres(in_memory_repo)
    assert len(genre_list) == 20

def test_can_get_all_years(in_memory_repo):
    year_list = movies_services.get_all_years(in_memory_repo)
    assert len(year_list) == 11

def test_can_get_related_movie_by_director_or_actor(in_memory_repo):
    movie_list = movies_services.get_related_movie('director','James Gunn',in_memory_repo)
    assert len(movie_list) == 3
    movie_list = movies_services.get_related_movie('actor', 'Dwayne Johnson', in_memory_repo)
    assert len(movie_list) == 10

def test_can_search(in_memory_repo):
    result_dict, count = movies_services.search('jack',in_memory_repo)
    assert count == 27
    result_dict1, count = movies_services.search(' JaCk', in_memory_repo)
    assert result_dict1 == result_dict
    result_dict2, count = movies_services.search(' JaCK ', in_memory_repo)
    assert result_dict2 == result_dict
    result_dict2, count = movies_services.search('ashdahsdiuahsd   ', in_memory_repo)
    assert result_dict2 == {}
