from pymongo import MongoClient


class Client:
    def __init__(self):
        self.client = MongoClient("localhost", 27017)
        self.db = self.client["MovieLibrary"]
        self.collection = self.db["movies"]

    def insert_movie(self, data):
        if not self.find_movie(data["id"]):
            self.collection.insert_one(data)
        else:
            self.collection.update_one({"id": data["id"]}, {"$set": data})

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