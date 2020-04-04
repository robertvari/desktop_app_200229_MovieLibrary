import requests, os, shutil


def get_image_data(image_url):
    response = requests.get(image_url)
    return response.content


def download_image(poster_folder, image_url):
    response = requests.get(image_url, stream=True)

    if response.status_code == 200:
        poster_file = os.path.join(poster_folder, image_url.split("/")[-1])

        if not os.path.exists(poster_folder):
            os.mkdir(poster_folder)

        with open(poster_file, "wb") as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)


if __name__ == '__main__':
    poster_folder = r"C:\Users\Robert\Downloads\Movie_Library"
    image_url = "https://image.tmdb.org/t/p/w300/8fDtXi6gVw8WUMWGT9XFz7YwkuE.jpg"
    download_image(poster_folder, image_url)