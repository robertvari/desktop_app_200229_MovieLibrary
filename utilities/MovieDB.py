import tmdbsimple as tmdb

tmdb.API_KEY = "83cbec0139273280b9a3f8ebc9e35ca9"
image_server = 'https://image.tmdb.org/t/p/w300'
search = tmdb.Search()
genre_list = tmdb.Genres().movie_list()


def find_movie(title, all_pages=False):
    response = search.movie(query=title, page=1)
    pages = response['total_pages']

    result_list = response["results"]
    if all_pages:
        for page in range(2, pages + 1):
            next_page_result = search.movie(query=title, page=page)
            result_list += next_page_result["results"]

    return [data for data in result_list if check_data_fields(data)]


def check_data_fields(data):
    release_date = data.get("release_date")
    poster_path = data.get("poster_path")

    if release_date and poster_path:
        return True
    return False


if __name__ == '__main__':
    result = find_movie("Alien")
    for i in result:
        if i.get("poster_path"):
            print(f"{image_server}{i.get('poster_path')}")