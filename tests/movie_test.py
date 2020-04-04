from unittest import TestCase
import os

from nodes.movie import Movie
from utilities.MovieDB import find_movie
from utilities.database import Client

movie_data = find_movie("Star Wars")[0]
client = Client()


class MovieTest(TestCase):

    def setUp(self) -> None:
        """Setup data for tests"""

    def tearDown(self) -> None:
        """Remove data, folders, files after tests"""


    def test_add_movie(self):
        movie = Movie(movie_data)
        movie.save()
        self.assertEqual()

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