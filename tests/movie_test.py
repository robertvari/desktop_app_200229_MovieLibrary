from unittest import TestCase
import os

from nodes.movie import Movie
from utilities.MovieDB import find_movie
from nodes.database import Client

movie_data = find_movie("Star Wars")[0]
client = Client()


class MovieTest(TestCase):

    def setUp(self) -> None:
        """Setup data for tests"""

    def tearDown(self) -> None:
        """Remove data, folders, files after tests"""

    def test_replace_poster(self):
        movie_data = client.find_movie(id=11)
        starwars_movie = Movie(movie_data)

        poster_path = r"C:\Users\Robert\Desktop\movie_posters\gladiator_poster.jpg"
        starwars_movie.set_poster(poster_path)

    def test_movie_data(self):
        all_movies = Movie.get_all()

        for movie in all_movies:
            try:
                print(movie.poster_path)
            except AttributeError:
                print("ERROR:", movie.__dict__)

    def test_has_movie(self):
        #  check if current movie has in database
        movie = Movie(movie_data)
        movie.save()

        self.assertIsNotNone(client.find_movie(movie_data["id"]))

    def test_add_movie(self):
        movie = Movie(movie_data)
        movie.save()

        # find movie in database
        result = client.find_movie(movie.id)
        self.assertIsNotNone(result)

        # test poster download
        poster_path = movie.get_poster()
        self.assertTrue(os.path.exists(poster_path))

        movie.delete()

    def test_set_favorited_movie(self):
        movie = Movie(movie_data)
        movie.save()

        movie.set_favorited(True)

        # check if database gets updated
        result = client.find_movie(movie.id)
        self.assertTrue(result["favorited"])

        movie.delete()

    def test_delete_movie(self):
        movie = Movie(movie_data)
        movie.save()

        poster_path = movie.get_poster()

        movie.delete()
        result = client.find_movie(movie.id)
        self.assertIsNone(result)

        self.assertFalse(os.path.exists(poster_path))