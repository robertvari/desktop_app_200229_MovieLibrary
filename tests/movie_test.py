from unittest import TestCase
import os

from nodes.movie import Movie
from utilities.MovieDB import find_movie
from utilities.database import Client

movie_data = find_movie("Star Wars")[0]
client = Client()


class MovieTest(TestCase):
    def test_add_movie(self):
        movie = Movie(movie_data)
        movie.save()

        # find movie in database
        result = client.find_movie(movie.id)
        self.assertIsNotNone(result)

        # test poster download
        poster_path = movie.get_poster()
        self.assertTrue(os.path.exists(poster_path))

    def test_edit_movie(self):
        print("test_edit_movie")

    def test_delete_movie(self):
        print("test_delete_movie")