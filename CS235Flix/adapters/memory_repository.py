import csv
import os
from datetime import datetime
from typing import List

from bisect import bisect_left, insort_left

from werkzeug.security import generate_password_hash

from CS235Flix.adapters.repository import AbstractRepository
from CS235Flix.domain.model import Actor, Director, Genre, Movie, Review, User, make_review


class MemoryRepository(AbstractRepository):
    # Movies ordered by rank.

    def __init__(self):
        self._movies = list()
        self._movies_index = dict()
        self._users = list()
        self._reviews = dict()
        self._movie_year = dict()
        self._movie_genre = dict()
        self._movie_actor = dict()
        self._movie_director = dict()
        self._genre_year = ['All', 'All']

    def update_genre_year(self, genre_year, value):
        if genre_year == 'genre':
            self._genre_year[0] = value
        else:
            self._genre_year[1] = value
        return self._genre_year

    def add_user(self, user: User):
        self._users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self._users if user.username == username), None)

    def add_movie(self, movie: Movie):
        insort_left(self._movies, movie)
        self._movies_index[movie.rank] = movie

    def add_year(self, dict_year):
        self._movie_year = dict_year

    def add_genres(self, dict_genre):
        self._movie_genre = dict_genre

    def add_director(self, dict_director):
        self._movie_director = dict_director

    def add_actor(self, dict_actor):
        self._movie_actor = dict_actor

    def get_genres(self):
        return self._movie_genre

    def get_years(self):
        return self._movie_year

    def get_actors(self):
        return self._movie_actor

    def get_directors(self):
        return self._movie_director

    def get_movies(self):
        return self._movies

    def get_movie(self, rank: int) -> Movie:
        movie = None
        try:
            movie = self._movies_index[rank]
        except KeyError:
            print("KeyError has been raised!")
            pass  # Ignore exception and return None.

        return movie

    def get_number_of_movies(self):
        return len(self._movies)

    def get_movies_by_year(self, year) -> List[Movie]:
        # Fetch the Movies.
        try:
            movies = self._movie_year[int(year)]
        except KeyError:
            print("KeyError has been raised!")
            pass  # Ignore exception and return None.
        return movies

    def get_movies_by_genre(self, genre):
        # Fetch the Movies.
        try:
            movies = self._movie_genre[Genre(genre)]
        except KeyError:
            print("KeyError has been raised!")
            pass  # Ignore exception and return None.
        return movies

    def get_movies_by_director(self, director):
        # Fetch the Movies.
        try:
            movies = self._movie_director[Director(director)]
        except KeyError:
            print("KeyError has been raised!")
            pass  # Ignore exception and return None.
        return movies

    def get_movies_by_actor(self, actor):
        # Fetch the Movies.
        try:
            movies = self._movie_actor[Actor(actor)]
        except KeyError:
            print("KeyError has been raised!")
            pass  # Ignore exception and return None.
        return movies

    def add_review(self, review: Review):
        if review.movie not in self._reviews:
            self._reviews[review.movie] = [review]
        else:
            self._reviews[review.movie].append(review)

    def get_reviews(self, rank: int):
        movie = self._movies_index[rank]
        if movie in self._reviews:
            return self._reviews[movie]
        else:
            return []

    # Helper method to return movie index.
    def movie_index(self, movie: Movie):
        index = bisect_left(self._movies, movie)
        if index != len(self._movies) and self._movies[index].year == movie.year:
            return index
        raise ValueError


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_movies(data_path: str, repo: MemoryRepository):
    dataset_of_movies = []
    dataset_of_actors = []
    dataset_of_directors = []
    dataset_of_genres = []
    dictionary_genres = {}  # extension
    dictionary_actors = {}  # extension
    dictionary_directors = {}  # extension
    dictionary_years = {}
    ignore_row=0
    for row in read_csv_file(os.path.join(data_path, 'Data1000Movies.csv')):
        if ignore_row==0:
            ignore_row+=1
            continue
        rank = int(row[0])
        title = row[1]
        genres = row[2].split(',')
        description = row[3]
        director = Director(str(row[4]))
        actors = row[5].split(',')
        release_year = int(row[6])
        runtime_minutes = int(row[7])
        rating = float(row[8])
        votes = int(row[9])
        revenue_millions = row[10]
        metascore = row[11]
        image_hyperlink = row[12]

        # create movie object
        movie = Movie(title, release_year)
        dataset_of_movies.append(movie)
        if movie.year not in dictionary_years:
            dictionary_years[movie.year] = [movie]  # extension
        else:
            dictionary_years[movie.year].append(movie)

        # add actors
        for actor in actors:
            actor_obj = Actor(actor)
            movie.add_actor(actor_obj)
            if actor_obj not in dataset_of_actors:
                dataset_of_actors.append(actor_obj)
                dictionary_actors[actor_obj] = [movie]  # extension
            else:
                dictionary_actors[actor_obj].append(movie)  # extension

        # add director
        movie.director = director
        if director not in dataset_of_directors:
            dataset_of_directors.append(director)
            dictionary_directors[director] = [movie]
        else:
            dictionary_directors[director].append(movie)

        # add genre
        for genre in genres:
            genre_obj = Genre(genre)
            movie.add_genre(genre_obj)
            if genre_obj not in dataset_of_genres:
                dataset_of_genres.append(genre_obj)
                dictionary_genres[genre_obj] = [movie]  # extension
            else:
                dictionary_genres[genre_obj].append(movie)  # extension

        # add description
        movie.description = description

        # add runtime
        movie.runtime_minutes = runtime_minutes

        # add rank
        movie.rank = rank

        # add rating
        movie.rating = rating

        # add votes
        movie.votes = votes

        # add revenue_million
        movie.revenue_millions = revenue_millions

        # add metascore
        movie.metascore = metascore

        # add metascore
        movie.image_hyperlink = image_hyperlink

        # Add the Movie to the repository.
        repo.add_movie(movie)

    repo.add_year(dictionary_years)
    repo.add_genres(dictionary_genres)
    repo.add_director(dictionary_directors)
    repo.add_actor(dictionary_actors)


def load_users(data_path: str, repo: MemoryRepository):
    users = dict()
    ignore_row = 0
    for data_row in read_csv_file(os.path.join(data_path, 'users.csv')):
        if ignore_row==0:
            ignore_row+=1
            continue
        user = User(
            username=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        repo.add_user(user)
        users[data_row[0]] = user
    return users


def load_reviews(data_path: str, repo: MemoryRepository, users):
    ignore_row = 0
    for data_row in read_csv_file(os.path.join(data_path, 'reviews.csv')):
        if ignore_row==0:
            ignore_row+=1
            continue
        review = make_review(
            review_text=data_row[3],
            user=users[data_row[1]],
            movie=repo.get_movie(int(data_row[2])),
            timestamp=datetime.fromisoformat(data_row[4]),
            rating=int(data_row[5])
        )
        repo.add_review(review)


def populate(data_path: str, repo: MemoryRepository):
    # Load movies and details into the repository.
    load_movies(data_path, repo)

    # Load users into the repository.
    users = load_users(data_path, repo)

    # Load comments into the repository.
    load_reviews(data_path, repo, users)
