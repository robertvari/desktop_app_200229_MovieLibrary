import requests, os, shutil

static_image_folder = os.path.join(os.path.dirname(__file__).replace("utilities", "static"), "images")


def get_static_image(image_name):
    static_path = os.path.join(static_image_folder, image_name)
    if os.path.exists(static_path):
        return static_path


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

        return poster_file


if __name__ == '__main__':
    print(get_static_image("no_poster.jpg"))