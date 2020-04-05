import tmdbsimple as tmdb

tmdb.API_KEY = "83cbec0139273280b9a3f8ebc9e35ca9"
search = tmdb.Search()
genre_list = tmdb.Genres().movie_list()


def find_movie(title):
    response = search.movie(query=title)
    return response["results"]


if __name__ == '__main__':
    from nodes.database import Client
    client = Client()

    result = find_movie("Titanic")[0]
    print(client.change_genre_ids(result))
