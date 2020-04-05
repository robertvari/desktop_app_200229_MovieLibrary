from pymongo import MongoClient
from utilities.MovieDB import genre_list


class Client:
    def __init__(self):
        self.client = MongoClient("localhost", 27017)
        self.db = self.client["MovieLibrary"]
        self.collection = self.db["movies"]
        self.genre_list = genre_list["genres"]

    def insert_movie(self, data):

        if not self.find_movie(data["id"]):
            # change id-s to names in genre_ids
            self.change_genre_ids(data)
            self.collection.insert_one(data)

        else:
            self.collection.update_one({"id": data["id"]}, {"$set": data})

    def change_genre_ids(self, data):
        id_list = data.get("genre_ids")

        genre_name = []
        for id in id_list:
            for i in self.genre_list:
                if i["id"] == id:
                    genre_name.append(i["name"])

        data["genre_ids"] = genre_name

    def get_release_dates(self):
        all_movies = self.get_movies()
        date_list = [i.get("release_date").split("-")[0] for i in all_movies]
        return sorted( list(set(date_list)), reverse=True)

    def get_languages(self):
        all_movies = self.get_movies()
        language_list = [i.get("original_language") for i in all_movies]
        return sorted(list(set(language_list)))

    def get_genres(self):
        all_movies = self.get_movies()
        all_genres = [i.get("genre_ids") for i in all_movies]

        genre_list = []
        for movie_genres in all_genres:
            [genre_list.append(i) for i in movie_genres if not i in genre_list]

        return sorted(genre_list)

    def find_movie(self, id):
        return self.collection.find_one({"id": id})

    def delete_movie(self, id):
        self.collection.delete_one({"id": id})

    def get_movies(self):
        return [i for i in self.collection.find()]


if __name__ == '__main__':
    database = Client()
    result = database.get_movies()
    print(result)