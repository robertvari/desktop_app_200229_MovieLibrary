from utilities.database import Client

client = Client()


class Movie:
    def __init__(self, data):
        for k, v in data.items():
            setattr(self, k, v)

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