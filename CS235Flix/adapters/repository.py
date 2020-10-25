import abc
from typing import List

from CS235Flix.domain.model import Movie, Review, User

repo_instance = None

class RepositoryException(Exception):

    def __init__(self, message=None):
        pass

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username) -> User:
        """ Returns the User named username from the repository.

        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def update_genre_year(self, genre_year, value):
        """ It updates the condition when genre or year is selected."""
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self, movie: Movie):
        """" Adds a Movie to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_year(self, dict_year):
        """" Adds a dictionary of year to the repository.

        It contains a list of movies that is related to a particular year
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_genres(self, dict_genre):
        """" Adds a dictionary of genre to the repository.

        It contains a list of movies that is related to a particular genre
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_director(self, dict_director):
        """" Adds a dictionary of director to the repository.

        It contains a list of movies that is related to a particular director
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_actor(self, dict_actor):
        """" Adds a dictionary of actors to the repository.

        It contains a list of movies that is related to a particular actor
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies(self) -> List:
        """ Returns a list of movies from the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self) -> Movie:
        """ Returns a movie by searching up the rank from the repository.

        If there is no movie with the given rank, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_movies(self) -> int:
        """ Returns number of the movies from the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_year(self, year):
        """ Returns a list of Movies which matches the target year from the repository.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_genre(self, genre):
        """ Returns a list of Movies which matches the genre from the repository.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    def get_movies_by_director(self, director):
        """ Returns a list of Movies which matches the director from the repository.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    def get_movies_by_actor(self, actor):
        """ Returns a list of Movies which matches the actor from the repository.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds a review to the repository.

        If the Review doesn't have bidirectional links with an Movie and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        if review.user is None or review not in review.user.reviews:
            raise RepositoryException('Review not correctly attached to a User')
        if review.movie is None or review not in review.movie.reviews:
            raise RepositoryException('Review not correctly attached to a Movie')

    @abc.abstractmethod
    def get_reviews(self):
        """ Returns the Reviews stored in the repository. """
        raise NotImplementedError
