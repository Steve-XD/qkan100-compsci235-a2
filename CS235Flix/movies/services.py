from typing import List, Iterable
from datetime import datetime
import random

from CS235Flix.adapters.repository import AbstractRepository
from CS235Flix.domain.model import make_review

class NonExistentMovieException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_review(rate: int, rank:int , review_text: str, username: str, repo: AbstractRepository):
    # Check that the article exists.
    movie = repo.get_movie(int(rank))
    print(movie)
    if movie is None:
        raise NonExistentMovieException

    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    timestamp= datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(timestamp)
    # Create comment.
    review = make_review(review_text, user, movie,timestamp, rate)
    # Update the repository.
    repo.add_review(review)


def get_11_movie(repo: AbstractRepository):
    movies = []

    for rank in range(1, 12):
        movies.append(repo.get_movie(rank))

    if movies is [] or len(movies) != 11:
        raise NonExistentMovieException

    return movies

def get_10_movie(condition, repo: AbstractRepository):
    movies = []
    #generate 10 random movies
    if condition == 'random':
        random_rank_list = random.sample(range(12, repo.get_number_of_movies() + 1), 10)
        for rank in random_rank_list:
            movies.append(repo.get_movie(rank))

    #all genres
    else:
        all_genre_movies = []
        for genre in condition:
            all_genre_movies += [movie for movie in repo.get_movies_by_genre(genre.genre_name) if movie not in all_genre_movies]
        if len(all_genre_movies) >= 10:
            random_index_list = random.sample(range(len(all_genre_movies)), 10)
        else: #less than 10 movies among all the genres
            random_index_list = random.sample(range(len(all_genre_movies)), len(all_genre_movies))
        for index in random_index_list:
            movies.append(all_genre_movies[index])

    if movies is []:
        raise NonExistentMovieException

    return movies

def get_movie(rank, repo: AbstractRepository):
    return repo.get_movie(int(rank))

def get_reviews(rank, repo: AbstractRepository):
    return repo.get_reviews(int(rank))

def get_all_movie(condition, repo: AbstractRepository):
    movies = []

    if condition[0] != 'All' and condition[1] != 'All':
        movies_genre = repo.get_movies_by_genre(condition[0])
        movies_year = repo.get_movies_by_year(condition[1])
        if len(movies_year) < len(movies_genre):
            for movie in movies_year:
                if movie in movies_genre:
                    movies.append(movie)
        else:
            for movie in movies_genre:
                if movie in movies_year:
                    movies.append(movie)

    elif condition == ['All','All']:
        for rank in range(1,repo.get_number_of_movies()+1):
            movies.append(repo.get_movie(int(rank)))

    else:
        index = condition.index('All')
        if index == 0:
            movies = repo.get_movies_by_year(condition[1])
        else:
            movies = repo.get_movies_by_genre(condition[0])

    if movies == []:
        return 'None'

    return movies

def get_all_genres(repo: AbstractRepository):
    genres = []

    for genre in repo.get_genres():
        genres.append(genre)

    if genres is []:
        raise NonExistentGenreException

    return sorted(genres)

def get_all_years(repo: AbstractRepository):
    years = []

    for year in repo.get_years():
        years.append(year)

    if years is []:
        raise NonExistentYearException

    return sorted(years, reverse = True)

def update_genre_year(genre_year, value, repo: AbstractRepository):
    return repo.update_genre_year(genre_year, value)

def get_related_movie(a_class, name, repo: AbstractRepository):
    if a_class == 'director':
        movies = repo.get_movies_by_director(name)
    else:
        movies = repo.get_movies_by_actor(name)

    return movies

def search(search_text, repo: AbstractRepository):
    result_dict = {}
    search_text = search_text.strip().lower()
    count = 0
    #find related movie
    for movie in repo.get_movies():
        if search_text in movie.title.lower():
            count+=1
            if "Movie" not in result_dict:
                result_dict["Movie"] = [movie]
            else:
                result_dict["Movie"].append(movie)
    #find related actor
    for actor in repo.get_actors():
        if search_text in actor.actor_full_name.lower():
            count += 1
            if "Actor" not in result_dict:
                result_dict["Actor"] = [actor]
            else:
                result_dict["Actor"].append(actor)
    #find related director
    for director in repo.get_directors():
        if search_text in director.director_full_name.lower():
            count += 1
            if "Director" not in result_dict:
                result_dict["Director"] = [director]
            else:
                result_dict["Director"].append(director)
    return result_dict, count
