import os

images_folder = os.path.join(os.path.dirname(__file__), "images")
posters = [os.path.join(images_folder, i) for i in os.listdir(images_folder)]

description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."



def create_dummy_data(number=10):
    import random
    movie_list = []

    titles = [
        "Shark",
        "Alien",
        "Terminator",
        "Star Wars",
        "Star Trek"
    ]

    years = [
        1970,
        1980,
        1990,
        2000,
        2010,
    ]

    genres = [
        "action",
        "comedy",
        "thriller",
        "horror",
        "sci-fi",
    ]

    for i in range(number):
        movie_list.append(
            {
                "title": random.choice(titles),
                "year": random.choice(years),
                "genre": random.choice(genres),
                "poster": random.choice(posters),
                "description": description
            }
        )

    return movie_list


if __name__ == '__main__':
    for m in create_dummy_data(20):
        print(m)