import tmdbsimple as tmdb

tmdb.API_KEY = "83cbec0139273280b9a3f8ebc9e35ca9"
search = tmdb.Search()


def find_movie(title):
    response = search.movie(query=title)
    return response["results"]


if __name__ == '__main__':
    for i in find_movie("Titanic"):
        print(i)