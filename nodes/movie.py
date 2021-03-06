from .database import Client
import os, requests, shutil, time

client = Client()
user_folder = os.path.join(os.path.expanduser(r"~"), "Downloads")
poster_folder = os.path.join(user_folder, "Movie_Library")

from utilities.image_utils import get_static_image


class Movie:
    server_path = 'https://image.tmdb.org/t/p/w300'

    def __init__(self, data):
        for k, v in data.items():
            setattr(self, k, v)

        if not hasattr(self, "favorited"):
            self.favorited = False

    def get_poster(self):
        if hasattr(self, "poster_path") and self.poster_path:
            poster_file = os.path.join(poster_folder, self.poster_path.replace("/", ""))

            if not os.path.exists(poster_file):
                poster_url = self.server_path + self.poster_path
                response = requests.get(poster_url, stream=True)

                if response.status_code == 200:
                    if not os.path.exists(poster_folder):
                        os.mkdir(poster_folder)

                    with open(poster_file, "wb") as f:
                        response.raw.decode_content = True
                        shutil.copyfileobj(response.raw, f)

            return poster_file

        return get_static_image("no_poster.jpg")

    def set_poster(self, new_poster_path):
        old_poster_path = self.get_poster()

        if old_poster_path:
            shutil.copyfile(new_poster_path, old_poster_path)

        else:
            old_poster_path = os.path.join(poster_folder, os.path.basename(new_poster_path))
            shutil.copyfile(new_poster_path, old_poster_path)

            self.porster_path = f"/{os.path.basename(new_poster_path)}"
            self.save()

    def get_filter_set(self):
        filter_set = {self.original_title}
        filter_set.update(self.genre_ids)
        filter_set.add(self.original_language)
        filter_set.add(self.release_date.split("-")[0])

        return filter_set

    def set_favorited(self, value):
        self.favorited = value
        self.save()

    def save(self):
        client.insert_movie(self.__dict__)

    def delete(self):
        client.delete_movie(self.id)
        if self.get_poster():
            os.remove(self.get_poster())

    @staticmethod
    def get_all():
        return [Movie(movie_data) for movie_data in client.get_movies()]

    def __str__(self):
        return f"{self.original_title} ({self.release_date})"

    def __repr__(self):
        return self.original_title


if __name__ == '__main__':
    print(poster_folder)