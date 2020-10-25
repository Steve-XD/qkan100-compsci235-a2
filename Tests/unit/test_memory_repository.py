from datetime import date, datetime
from typing import List

import pytest

from CS235Flix.adapters.repository import AbstractRepository, RepositoryException
from CS235Flix.domain.model import Actor, Director, Genre, Movie, Review, User, WatchList, make_review

def test_repository_can_add_a_user(in_memory_repo):
    user = User('Dave', '123456789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('Dave') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_movie_count(in_memory_repo):
    number_of_movies = in_memory_repo.get_number_of_movies()

    # Check that the query returned all movies in csv which is 1000 Movies.
    assert number_of_movies == 1000


def test_repository_can_add_movie(in_memory_repo):
    movie = Movie(
        "I am Legend",
        1981
    )
    movie.rank = 1001
    in_memory_repo.add_movie(movie)
    assert in_memory_repo.get_movie(1001) is movie

def test_repository_can_add_year_dict(in_memory_repo):
    movie = Movie(
        "I am Legend",
        1981
    )
    dict_year = {}
    dict_year[movie.year]=movie
    in_memory_repo.add_year(dict_year)
    assert in_memory_repo.get_years() is dict_year

def test_repository_can_add_genre_dict(in_memory_repo):
    movie = Movie(
        "I am Legend",
        1981
    )
    genre = Genre("Fantasy")
    movie.genres=genre
    dict_genre = {}
    dict_genre[genre]=[movie]
    in_memory_repo.add_genres(dict_genre)
    assert in_memory_repo.get_genres() is dict_genre

def test_repository_can_add_actor_dict(in_memory_repo):
    movie = Movie(
        "I am Legend",
        1981
    )
    actor = Actor("Will Smith")
    movie.actors=actor
    dict_actor = {}
    dict_actor[actor]=[movie]
    in_memory_repo.add_actor(dict_actor)
    assert in_memory_repo.get_actors() is dict_actor

def test_repository_can_add_director_dict(in_memory_repo):
    movie = Movie(
        "I am Legend",
        1981
    )
    director = Director("James Gunn")
    movie.director=director
    dict_director = {}
    dict_director[director]=[movie]
    in_memory_repo.add_director(dict_director)
    assert in_memory_repo.get_directors() is dict_director

def test_repository_can_retrieve_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(1)

    # Check that the Movie has the expected title.
    assert movie.title == 'Guardians of the Galaxy'

    # Check that the Movie is commented as expected.
    review_one = [review for review in movie.reviews if review.review_text == "This movie is fantastic!"][0]
    review_two = [review for review in movie.reviews if review.review_text == "Yeah Freddie, good movie!"][0]
    assert review_one.user.username == 'fmercury'
    assert review_two.user.username == "thorke"

    # # Check that the Movie is tagged as expected.
    assert movie.is_tagged_by(Genre('Action'))
    assert movie.is_tagged_by(Genre('Adventure'))


def test_repository_does_not_retrieve_a_non_existent_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(1001)
    assert movie is None


def test_repository_can_retrieve_movies_by_date(in_memory_repo):
    movies = in_memory_repo.get_movies_by_year(2009)

    # Check that the query returned 51 Articles.
    assert len(movies) == 51

    movies = in_memory_repo.get_movies_by_year(2010)
    assert len(movies) == 60

def test_repository_can_retrieve_movies_by_genre(in_memory_repo):
    movies = in_memory_repo.get_movies_by_genre('Fantasy')

    # Check that the query returned 51 Articles.
    assert len(movies) == 101

    movies = in_memory_repo.get_movies_by_genre('Action')
    assert len(movies) == 303

def test_repository_can_retrieve_movies_by_director(in_memory_repo):
    movies = in_memory_repo.get_movies_by_director('James Gunn')

    # Check that the query returned 51 Articles.
    assert len(movies) == 3

def test_repository_can_retrieve_movies_by_actor(in_memory_repo):
    movies = in_memory_repo.get_movies_by_actor('Dwayne Johnson')

    # Check that the query returned 51 Articles.
    assert len(movies) == 10

def test_repository_retrieve_movie_image(in_memory_repo):
    movie = in_memory_repo.get_movie(1)
    hyperlink = movie.image_hyperlink
    assert hyperlink == "https://m.media-amazon.com/images/M/MV5BMTAwMjU5OTgxNjZeQTJeQWpwZ15BbWU4MDUxNDYxODEx._V1_SX300.jpg"

def test_repository_can_add_a_review(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    movie = in_memory_repo.get_movie(1)
    timestamp= datetime.today()
    review = make_review("Trump's onto it!", user, movie, timestamp,5)

    in_memory_repo.add_review(review)

    assert review in in_memory_repo.get_reviews(1)

def test_repository_can_retrieve_comments(in_memory_repo):
    assert len(in_memory_repo.get_reviews(1)) == 3


