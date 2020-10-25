from datetime import datetime

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, SelectField, StringField
from wtforms.validators import DataRequired, Length, ValidationError

import CS235Flix.adapters.repository as repo
import CS235Flix.movies.services as services

from CS235Flix.authentication.authentication import login_required

# Configure Blueprint.
movies_blueprint = Blueprint(
    'movies_bp', __name__)


@movies_blueprint.route('/home', methods=['GET', 'POST'])
@login_required
def login_home():
    timestamp = datetime.now().strftime("%H")
    username = session['username']
    if 5 <= int(timestamp) < 12:
        greeting = "Good Morning"
    elif 12 <= int(timestamp) < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"
    get_first_11_movies = services.get_11_movie(repo.repo_instance)
    get_random_10_movies = services.get_10_movie('random', repo.repo_instance)
    form = SearchForm()
    if form.validate_on_submit():
        # Successful POST, i.e. the search text has passed data validation.
        return redirect(url_for('movies_bp.movie_search', search_text=form.search.data))

    return render_template(
        'Second/home/home.html',
        title='Home',
        popular_movie=get_first_11_movies,
        random_movie=get_random_10_movies,
        greeting=greeting,
        username=username,
        form=form,
        handler_url=url_for('movies_bp.login_home')
    )


@movies_blueprint.route('/movie-detail/<rank>', methods=['GET', 'POST'])
@login_required
def movie_detail(rank):
    movie_obj = services.get_movie(rank, repo.repo_instance)
    reviews = services.get_reviews(rank, repo.repo_instance)
    all_genre = movie_obj.genres
    get_random_10_movies = services.get_10_movie(all_genre, repo.repo_instance)
    form = SearchForm()
    if form.validate_on_submit():
        # Successful POST, i.e. the search text has passed data validation.
        return redirect(url_for('movies_bp.movie_search', search_text=form.search.data))
    return render_template(
        'Second/movie_info/movie_info.html',
        title=movie_obj.title + ' (' + str(movie_obj.year) + ')',
        movie=movie_obj,
        random_movie=get_random_10_movies,
        reviews=reviews,
        reviews_count=len(reviews),
        form=form,
        handler_url=url_for('movies_bp.movie_detail', rank=rank)
    )


@movies_blueprint.route('/all-movie/<genre>/<year>', methods=['GET', 'POST'])
@login_required
def list_all_movie(genre, year):
    genres = services.get_all_genres(repo.repo_instance)
    years = services.get_all_years(repo.repo_instance)

    condition = [genre, year]
    if request.form.get("genre") != None:
        condition = services.update_genre_year('genre', request.form.get("genre"), repo.repo_instance)
    elif request.form.get("year") != None:
        condition = services.update_genre_year('year', request.form.get("year"), repo.repo_instance)
    else:  # update the condition
        services.update_genre_year('genre', genre, repo.repo_instance)
        services.update_genre_year('year', year, repo.repo_instance)
    movies = services.get_all_movie(condition, repo.repo_instance)
    form = SearchForm()
    if form.validate_on_submit():
        # Successful POST, i.e. the search text has passed data validation.
        return redirect(url_for('movies_bp.movie_search', search_text=form.search.data))

    return render_template(
        'Second/movie_info/all_movie.html',
        title='all_movie',
        movies=movies,
        genres_condition=condition[0],
        year_condition=condition[1],
        genres=genres,
        years=years,
        form=form,
        handler_url=url_for('movies_bp.list_all_movie', genre=genre, year=year)
    )


@movies_blueprint.route('/display/<a_class>/<name>', methods=['GET', 'POST'])
@login_required
def movie_director_actor(a_class, name):
    movies = services.get_related_movie(a_class, name, repo.repo_instance)
    title = '{} {}'.format(a_class, name)
    form = SearchForm()
    if form.validate_on_submit():
        # Successful POST, i.e. the search text has passed data validation.
        return redirect(url_for('movies_bp.movie_search', search_text=form.search.data))
    return render_template(
        'Second/movie_info/actor_director.html',
        title=title,
        movies=movies,
        name=name,
        a_class=a_class.title(),
        form=form,
        handler_url=url_for('movies_bp.movie_director_actor', a_class=a_class, name=name)
    )


@movies_blueprint.route('/play/<movie_name>/<rank>', methods=['GET', 'POST'])
@login_required
def movie_play(movie_name, rank):
    # Obtain the username of the currently logged in user.
    username = session['username']
    form = CommentForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the comment text has passed data validation.
        services.add_review(form.rate.data, rank, form.comment.data, username, repo.repo_instance)
        return redirect(url_for('movies_bp.login_home'))
    return render_template(
        'Second/movie_info/play.html',
        title="(Play) " + movie_name,
        movie_name=movie_name,
        form=form,
        handler_url=url_for('movies_bp.movie_play', movie_name=movie_name, rank=rank)
    )


@movies_blueprint.route('/search_result/<search_text>', methods=['GET', 'POST'])
@login_required
def movie_search(search_text):
    search_dict, result_count = services.search(search_text, repo.repo_instance)
    form = SearchForm()
    if form.validate_on_submit():
        # Successful POST, i.e. the search text has passed data validation.
        return redirect(url_for('movies_bp.movie_search', search_text=form.search.data))

    return render_template(
        'Second/movie_info/search.html',
        title="Search result",
        search_text=search_text,
        search_dict=search_dict,
        result_count=result_count,
        form=form,
        handler_url=url_for('movies_bp.movie_search', search_text=search_text)
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class CommentForm(FlaskForm):
    rate = SelectField('Rating', choices=[10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0])
    comment = TextAreaField('Comment', [
        DataRequired(),
        Length(min=4, message='Your comment is too short'),
        ProfanityFree(message='Your comment must not contain profanity')])
    movie_id = HiddenField("Movie id")
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    search = StringField('Search', [
        DataRequired(),
        Length(min=3, message='Please insert 3 or more letters'), ])
    submit = SubmitField('Submit')
