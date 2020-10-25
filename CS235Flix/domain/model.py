from datetime import datetime

class Actor:

    def __init__(self, actor_full_name : str):
        self.colleagues = []

        if actor_full_name  == "" or type(actor_full_name ) is not str:
            self.__actor_full_name  = None
        else:
            self.__actor_full_name  = actor_full_name .strip()

    @property
    def actor_full_name (self) -> str:
        return self.__actor_full_name

    def __repr__(self):
        return f"<Actor {self.__actor_full_name}>"

    def __eq__(self, other):
        return self.__actor_full_name  == other.__actor_full_name

    def __lt__(self, other):
        return self.__actor_full_name  < other.__actor_full_name

    def __hash__(self):
        return hash(self.__actor_full_name )

    def add_actor_colleague(self, other):
        self.colleagues.append(other)

    def check_if_this_actor_worked_with(self, other):
        return other in self.colleagues

class Director:

    def __init__(self, director_full_name: str):
        if director_full_name == "" or type(director_full_name) is not str:
            self.__director_full_name = None
        else:
            self.__director_full_name = director_full_name.strip()

    @property
    def director_full_name(self) -> str:
        return self.__director_full_name

    def __repr__(self):
        return f"<Director {self.__director_full_name}>"

    def __eq__(self, other):
        return self.__director_full_name == other.__director_full_name

    def __lt__(self, other):
        return self.__director_full_name < other.__director_full_name

    def __hash__(self):
        return hash(self.__director_full_name)

class Genre:

    def __init__(self, genre_name : str):
        if genre_name  == "" or type(genre_name ) is not str:
            self.__genre_name  = None
        else:
            self.__genre_name  = genre_name.strip()

    @property
    def genre_name(self) -> str:
        return self.__genre_name

    def __repr__(self):
        return f"<Genre {self.__genre_name}>"

    def __eq__(self, other):
        return self.__genre_name == other.__genre_name

    def __lt__(self, other):
        return self.__genre_name < other.__genre_name

    def __hash__(self):
        return hash(self.__genre_name)

class Movie:

    def __init__(self, title : str, year : int):
        self.__description = None
        self.__director = None
        self.__actors = []
        self.__genres = []
        self.__runtime_minutes = None
        self.__rank = None
        self.__rating = None
        self.__votes = None
        self.__revenue_millions = None
        self.__metascore = None
        self.__reviews = []
        self.__image_hyperlink = None

        if title == "" or type(title) is not str or year < 1900 or type(year ) is not int:
            self.__title   = None
            self.__year = None
        else:
            self.__title = title.strip()
            self.__year = year

    @property
    def title(self) -> str:
        return self.__title

    @property
    def year(self) -> str:
        return self.__year

    @property
    def description(self):
        return self.__description

    @property
    def director(self):
        return self.__director

    @property
    def actors(self):
        return self.__actors

    @property
    def genres(self):
        return self.__genres

    @property
    def runtime_minutes(self):
        return self.__runtime_minutes

    @property
    def image_hyperlink(self) -> str:
        return self.__image_hyperlink

    @title.setter
    def title(self, title):
        if title != "" and type(title) is str:
            self.__title = title.strip()

    @year.setter
    def year(self, year):
        if type(year) is int and year >= 1900:
            self.__year = year
        else:
            raise ValueError("ValueError exception thrown")

    @description.setter
    def description(self, description):
        if description != "" and type(description) is str:
            self.__description = description.strip()

    @director.setter
    def director(self, director):
        if isinstance(director, Director):
            self.__director = director

    @actors.setter
    def actors(self, actor):
        if isinstance(actor, Actor):
            self.__actors = [actor]

    @genres.setter
    def genres(self, genre):
        if isinstance(genre, Genre):
            self.__genres = [genre]

    @runtime_minutes.setter
    def runtime_minutes(self, runtime_minutes):
        if type(runtime_minutes) is int and runtime_minutes > 0:
            self.__runtime_minutes = runtime_minutes
        else:
            raise ValueError("ValueError exception thrown")

    @image_hyperlink.setter
    def image_hyperlink(self, image_hyperlink:str) -> str:
            self.__image_hyperlink = image_hyperlink

    def __repr__(self):
        return f"<Movie {self.__title}, {self.__year}>"

    def __eq__(self, other):
        return self.__title  == other.__title and self.__year == other.__year

    def __lt__(self, other):
        return (self.__title, self.__year) < (other.__title, other.__year)

    def __hash__(self):
        return hash((self.__title, self.__year))

    def add_actor(self, actor):
        if isinstance(actor, Actor):
            self.__actors.append(actor)

    def remove_actor(self, actor):
        if isinstance(actor, Actor) and actor in self.__actors:
            self.__actors.pop(self.__actors.index(actor))

    def add_genre(self, genre):
        if isinstance(genre, Genre):
            self.__genres.append(genre)

    def remove_genre(self, genre):
        if isinstance(genre, Genre) and genre in self.__genres:
            self.__genres.pop(self.__genres.index(genre))

    def is_tagged_by(self, genre):
        return genre in self.__genres

    ###################################### extension ######################################
    @property
    def year(self):
        return self.__year

    @property
    def rank(self):
        return self.__rank

    @property
    def rating(self):
        return self.__rating

    @property
    def votes(self):
        return self.__votes

    @property
    def revenue_millions(self):
        return self.__revenue_millions

    @property
    def metascore(self):
        return self.__metascore

    @property
    def reviews(self):
        return iter(self.__reviews)

    @year.setter
    def year(self, year):
        if type(year) is int and year >= 1900:
            self.__year = year
        else:
            raise ValueError("ValueError exception thrown")

    @rank.setter
    def rank(self, rank):
        if type(rank) is int and rank >= 0:
            self.__rank = rank
        else:
            raise ValueError("ValueError exception thrown")

    @rating.setter
    def rating(self, rating):
        if 0 <= rating <= 10:
            self.__rating = rating
        else:
            raise ValueError("ValueError exception thrown")

    @votes.setter
    def votes(self, votes):
        if type(votes) is int and votes >= 0:
            self.__votes = votes
        else:
            raise ValueError("ValueError exception thrown")

    @revenue_millions.setter
    def revenue_millions(self, revenue_millions):
        if revenue_millions == "N/A":
            self.__revenue_millions = "N/A"
        elif float(revenue_millions) >= 0:
            self.__revenue_millions = float(revenue_millions)
        else:
            raise ValueError("ValueError exception thrown")

    @metascore.setter
    def metascore(self, metascore):
        if metascore == "N/A":
            self.__metascore = "N/A"
        elif 0 <= float(metascore) <= 100:
            self.__metascore = float(metascore)
        else:
            raise ValueError("ValueError exception thrown")

    @reviews.setter
    def reviews(self, reviews):
        if isinstance(reviews, Review):
            self.__reviews = [reviews]

    def add_review(self, review):
        if isinstance(review, Review):
            self.__reviews.append(review)

class User:
    def __init__(self, username: str, password: str):
        self.__watched_movies = []
        self.__reviews = []
        self.__time_spent_watching_movies_minutes = 0
        self.__username: str = username
        self.__password: str = password

    @property
    def username(self):
        return self.__username

    @property
    def password (self):
        return self.__password

    @property
    def watched_movies (self):
        return self.__watched_movies

    @property
    def reviews(self):
        return self.__reviews

    @property
    def time_spent_watching_movies_minutes(self):
        return self.__time_spent_watching_movies_minutes

    @username.setter
    def username(self, user_name):
        if user_name != "" and type(user_name) is str:
            self.__username = user_name.strip()

    @password.setter
    def password(self, password):
        if password != "" and type(password) is str:
            self.__password = password

    @watched_movies.setter
    def watched_movies(self, watched_movies):
        if isinstance(watched_movies, Movie):
            self.__watched_movies = [watched_movies]

    @reviews.setter
    def reviews(self, reviews):
        if isinstance(reviews, Review):
            self.__reviews = [reviews]

    @time_spent_watching_movies_minutes.setter
    def time_spent_watching_movies_minutes(self, time_spent_watching_movies_minutes):
        if type(time_spent_watching_movies_minutes) is int and time_spent_watching_movies_minutes >= 0:
            self.__time_spent_watching_movies_minutes = time_spent_watching_movies_minutes

    def __repr__(self):
        return f'<User {self.__username} {self.__password}>'

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return other.__username.lower() == self.__username.lower()

    def __lt__(self, other):
        return self.__username.lower() < other.__username.lower()

    def __hash__(self):
        return hash(self.__username.lower())

    def watch_movie(self, movie):
        if isinstance(movie, Movie):
            self.__watched_movies.append(movie)
            self.__time_spent_watching_movies_minutes += movie.runtime_minutes

    def add_review(self, review):
        if isinstance(review, Review):
            self.__reviews.append(review)

class Review:
    def __init__(self, user:User, movie:Movie, review_text: str, timestamp: datetime, rating: int):
            self.__user = user
            self.__movie = movie
            self.__review_text = review_text.strip()
            self.__rating = rating
            self.__timestamp = timestamp

    @property
    def user(self):
        return self.__user

    @property
    def movie(self):
        return self.__movie

    @property
    def review_text(self):
        return self.__review_text

    @property
    def rating(self):
        return self.__rating

    @property
    def timestamp(self):
        return self.__timestamp

    @user.setter
    def user(self, user):
        if isinstance(user, User):
            self.__user = user

    @movie.setter
    def movie(self, movie):
        if isinstance(movie, Movie):
            self.__movie = movie

    @review_text.setter
    def review_text(self, review_text):
        if review_text != "" and type(review_text) is str:
            self.__review_text = review_text.strip()

    @rating.setter
    def rating(self, rating):
        if type(rating) is int and 1 <= rating <= 10:
            self.__rating = rating

    @timestamp.setter
    def timestamp(self, timestamp):
        self.__timestamp = timestamp

    def __repr__(self):
        return f"<Review ({self.__rating}/10):{self.__review_text}>"

    def __eq__(self, other):
        return self.__movie == other.__movie and self.__review_text == other.__review_text and \
               self.__rating == other.__rating and self.__timestamp == other.__timestamp



class WatchList:
    def __init__(self):
        self.__movie = []


    def add_movie(self, movie):
        if movie not in self.__movie:
            self.__movie.append(movie)

    def remove_movie(self, movie):
        if movie in self.__movie and isinstance(movie, Movie):
            self.__movie.pop(self.__movie.index(movie))

    def select_movie_to_watch(self, index):
        if index < len(self.__movie):
            return self.__movie[index]
        else:
            return None

    def size(self):
        return len(self.__movie)

    def first_movie_in_watchlist(self):
        if self.__movie == []:
            return None
        else:
            return self.__movie[0]

    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self):
        if self.__index < len(self.__movie):
            self.__index += 1
            return self.__movie[self.__index - 1]
        else:
            raise StopIteration

def make_review(review_text: str, user: User, movie: Movie, timestamp: datetime, rating:int):
    review = Review(user, movie, review_text, timestamp, rating)
    user.add_review(review)
    movie.add_review(review)

    return review