from pymongo import MongoClient


class Client:
    def __init__(self):
        self.client = MongoClient("localhost", 27017)
        self.db = self.client["MovieLibrary"]
        self.collection = self.db["movies"]

    def insert_movie(self, data):
        self.collection.insert_one(data)

    def get_movies(self):
        return [i for i in self.collection.find()]


if __name__ == '__main__':
    database = Client()
    result = database.get_movies()
    print(result)