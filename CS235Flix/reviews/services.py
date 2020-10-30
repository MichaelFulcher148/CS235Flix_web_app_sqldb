from CS235Flix.common import search_for_user
from CS235Flix.memory_repository.abtractrepository import AbstractRepository
from obj.movie import Review, Movie

def add_review(user_name: str, movie_title: str, movie_release_date: int, review_text: str, rating_num: int, repo: 'AbstractRepository'):
    a_movie = Movie(movie_title, movie_release_date)
    a_user = search_for_user(user_name, repo)
    if a_user:
        for movie in repo.get_movies():
            if movie == a_movie:
                a_movie = movie
                break
        new_review = Review(a_movie, review_text, rating_num)
        new_review.user = a_user
        a_user.add_review(new_review)
        repo.add_review(new_review)

def get_reviews(title: str, date: int, repo: 'AbstractRepository'):
    reviews_data = list()
    for user in repo.get_users():
        for review in user.reviews:
            if review.movie.title == title and review.movie.release_year == date:
                a_review = dict()
                a_review['text'] = review.review_text
                a_review['rating'] = review.rating
                a_review['date'] = review.timestamp.strftime('%d-%m-%Y %H:%M:%S')
                a_review['author'] = user.username
                reviews_data.append(a_review)
                break
    if len(reviews_data) > 0:
        reviews_data.reverse()
        return reviews_data
    else:
        return None
