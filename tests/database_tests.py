from unittest import TestCase

from nodes.database import Client
client = Client()


class DatabaseTests(TestCase):
    def test_list_dates(self):
        release_dates = client.get_release_dates()
        print(release_dates)

    def test_list_languages(self):
        language_list = client.get_languages()
        print(language_list)

    def test_genre_list(self):
        genre_list = client.get_genres()
        print(genre_list)