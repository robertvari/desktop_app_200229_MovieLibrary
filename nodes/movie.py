from utilities.database import Client
import os, requests, shutil

client = Client()
user_folder = os.path.join(os.path.expanduser(r"~"), "Downloads")
poster_folder = os.path.join(user_folder, "Movie_Library")

class Movie:
    server_path = 'https://image.tmdb.org/t/p/w300'

    def __init__(self, data):
        for k, v in data.items():
            setattr(self, k, v)

    def get_poster(self):
        if hasattr(self, "poster_path"):
            poster_file = os.path.join(poster_folder, self.poster_path.replace("/", ""))

            if not os.path.exists(poster_file):
                print("Downloading new poster...")
                poster_url = self.server_path + self.poster_path
                response = requests.get(poster_url, stream=True)

                if response.status_code == 200:
                    if not os.path.exists(poster_folder):
                        os.mkdir(poster_folder)


                    with open(poster_file, "wb") as f:
                        response.raw.decode_content = True
                        shutil.copyfileobj(response.raw, f)

            return poster_file

    def save(self):
        client.insert_movie(self.__dict__)

    def delete(self):
        pass

    def edit(self):
        pass

    @staticmethod
    def get_all():
        return [Movie(item) for item in client.get_movies()]

    def __str__(self):
        return f"{self.original_title} ({self.release_date})"

    def __repr__(self):
        return self.original_title


if __name__ == '__main__':
    print(poster_folder)