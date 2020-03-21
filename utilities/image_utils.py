import requests


def get_image_data(image_url):
    response = requests.get(image_url)
    return response.content


if __name__ == '__main__':
    get_image_data("https://image.tmdb.org/t/p/w300/8fDtXi6gVw8WUMWGT9XFz7YwkuE.jpg")