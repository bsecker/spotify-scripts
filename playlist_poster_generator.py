# Playlist Poster Generator
# outputs a png poster of all the albums in an inputted playlist
import spotipy
import configargparse
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import logging
import requests
import shutil
import os
from PIL import Image, ImageDraw, ImageFont

logging.basicConfig(level=logging.INFO)

SCOPE = 'playlist-modify-public'
DOWNLOAD_FOLDER = "download"

cache = ['https://i.scdn.co/image/ab67616d0000b273de437d960dda1ac0a3586d97',
         'https://i.scdn.co/image/ab67616d0000b273299e8e9983e2b0455e5e8505',
         'https://i.scdn.co/image/ab67616d0000b273ea9dc98a9ae5397ee3d6fb5a',
         'https://i.scdn.co/image/ab67616d0000b2735f704d655196fa4d21a968a0',
         'https://i.scdn.co/image/ab67616d0000b273484d121f0e2d2caf87d5d10b',
         'https://i.scdn.co/image/ab67616d0000b273285a20206dd6be33f04b29f4',
         'https://i.scdn.co/image/ab67616d0000b273358ad765aef7d4c598f913f0',
         'https://i.scdn.co/image/ab67616d0000b2739853ba3461b96cab41a56a11',
         'https://i.scdn.co/image/ab67616d0000b2739f1f05adbc6646a14e11fb39',
         'https://i.scdn.co/image/ab67616d0000b2738c4e95986c803791125e8991',
         'https://i.scdn.co/image/ab67616d0000b273104f8708597b5e11ab7296a2',
         'https://i.scdn.co/image/ab67616d0000b273a1128eef5ae9e18d84086bf3',
         'https://i.scdn.co/image/ab67616d0000b27371aca2afe20392971e4fbd08',
         'https://i.scdn.co/image/ab67616d0000b2732b16992e49be4a199e7dad2c',
         'https://i.scdn.co/image/ab67616d0000b273f6a7914d9d654bc3ca99a535',
         'https://i.scdn.co/image/ab67616d0000b273f15eb1683ae79b0b3f2bdf4e',
         'https://i.scdn.co/image/ab67616d0000b2730b51f8d91f3a21e8426361ae',
         'https://i.scdn.co/image/ab67616d0000b2738ac778cc7d88779f74d33311',
         'https://i.scdn.co/image/ab67616d0000b27304b250958af783eae5fbecd5',
         'https://i.scdn.co/image/ab67616d0000b273bc7e3632e2e40d5a026bbecb',
         'https://i.scdn.co/image/ab67616d0000b27326f7709399913201ebe40eee',
         'https://i.scdn.co/image/ab67616d0000b2738b56fd8fb9f486c7ebd2303a',
         'https://i.scdn.co/image/ab67616d0000b2737bd54d342d0cce6afa695c0b',
         'https://i.scdn.co/image/ab67616d0000b273c1c82c472d758f4945ac15a8',
         'https://i.scdn.co/image/ab67616d0000b273ab7c33d85dc21acb98f049f5',
         'https://i.scdn.co/image/ab67616d0000b273c41f4e1133b0e6c5fcf58680',
         'https://i.scdn.co/image/ab67616d0000b273b72abf1891a8eb90a92cd19d',
         'https://i.scdn.co/image/ab67616d0000b27378378dcaccec9e965e0d6351',
         'https://i.scdn.co/image/ab67616d0000b2739d3ca716cab9618d525be64d',
         'https://i.scdn.co/image/ab67616d0000b27369471a9c0a6073a9beb81410',
         'https://i.scdn.co/image/ab67616d0000b273a02118e3d404aebd8b3a017e',
         'https://i.scdn.co/image/ab67616d0000b2732b98de5962c1daedd20cc42d',
         'https://i.scdn.co/image/ab67616d0000b2734111af27787499f6d8752e9f',
         'https://i.scdn.co/image/ab67616d0000b2739ca0155f0b8223f4af20157a',
         'https://i.scdn.co/image/ab67616d0000b27384c7c218b54fddc1c80f41d5',
         'https://i.scdn.co/image/ab67616d0000b273da23c72ab18503218dc313b9',
         'https://i.scdn.co/image/ab67616d0000b27366709f6474296b865983f4d6',
         'https://i.scdn.co/image/ab67616d0000b27327cfc70113b48e2ab1a0e217',
         'https://i.scdn.co/image/ab67616d0000b2738058c873c88c1740994a9182',
         'https://i.scdn.co/image/ab67616d0000b273a1eb8cc749fd91f97849553f',
         'https://i.scdn.co/image/ab67616d0000b2732d912c59999754147fcb40e3',
         'https://i.scdn.co/image/ab67616d0000b273030915ffa58125ae36f13a6f',
         'https://i.scdn.co/image/ab67616d0000b273889efa7e898e5b3aca7eb800',
         'https://i.scdn.co/image/ab67616d0000b2730f0e452356e1a53b1475d3a2',
         'https://i.scdn.co/image/ab67616d0000b27302add2c77fb6999e311a3248',
         'https://i.scdn.co/image/ab67616d0000b273355bf68fa788b6d401195b43',
         'https://i.scdn.co/image/ab67616d0000b2730a2b491a06f9c0c165baca37',
         'https://i.scdn.co/image/ab67616d0000b273a45a839cb6f2ee4f0b10505f',
         'https://i.scdn.co/image/ab67616d0000b27395f58826ccc51a70f80a0344',
         'https://i.scdn.co/image/ab67616d0000b273df0aa104081c00b29aaa19ec',
         'https://i.scdn.co/image/ab67616d0000b273e9fc848924f30c739ff693a8',
         'https://i.scdn.co/image/ab67616d0000b2734824c01e17b7d67db29bf273',
         'https://i.scdn.co/image/ab67616d0000b2739b4c52f85f227508375e69c6',
         'https://i.scdn.co/image/ab67616d0000b273a949df0e18e6405dbd0f3bbc',
         'https://i.scdn.co/image/ab67616d0000b27387e9ef0f7d94bb6b7c4a7e13',
         'https://i.scdn.co/image/ab67616d0000b27337eebf484446eeb741ca32d1',
         'https://i.scdn.co/image/ab67616d0000b273535ce3ba3ab60c1336110b29',
         'https://i.scdn.co/image/ab67616d0000b2736e5492a25e67c5932981b03a',
         'https://i.scdn.co/image/ab67616d0000b273ce7b647fbb4e137ba39ad271',
         'https://i.scdn.co/image/ab67616d0000b273350ce5a5a1a107304a754cc0',
         'https://i.scdn.co/image/ab67616d0000b273f05e5ac32fdd79d100315a20',
         'https://i.scdn.co/image/ab67616d0000b2737f2765a77c845a9608da2ed0',
         'https://i.scdn.co/image/ab67616d0000b2734895aa42488369ec7f87ab91',
         'https://i.scdn.co/image/ab67616d0000b273207dd27959f179f42b01ab18',
         'https://i.scdn.co/image/ab67616d0000b273f9b1b466f3f6f5c25e852dd5',
         'https://i.scdn.co/image/ab67616d0000b2732ebd53589d4156e242398fa5',
         'https://i.scdn.co/image/ab67616d0000b2733cb1d402ce635f569adef111',
         'https://i.scdn.co/image/ab67616d0000b273dc9b0131146fe8798c3f46ed']

cached_average_rating = [7.5, 8, 6, 5.5, 5.5, 8, 6.5, 6, 5.5, 8, 2, 5.5, 7, 7, 5.5, 7, 9, 8, 6.5, 6.5, 1.5, 8.5, 7, 7.5,
                         8, 5, 6.5, 7, 8, 7, 4, 7, 7, 7, 4.5, 7.5, 8.5, 4.5, 6.5, 5.5, 7.5, 7, 7.5, 6.5, 9, 7.5, 6.5, 5,
                         7, 5.5, 5.5, 6.5, 5, 6, 8, 8, 8, 8, 6.5, 4.5, 6.5, 6, 5.5, 8.5, 3.5, 4.5, 7, 9.5, 6.5, 5.5,
                         5.5, 7.5, 5.5, 8.5, 7, 7.5, 4.5, 7.5, 8, 4.5, 7.5, 4, 5, 6.5, 3, 7, 4, 6, 8.5, 8, 5.5, 8.5,
                         5.5, 8, 6, 2.5, 4.5, 9.5, 8]


def retrieve_album_art_urls(sp, playlist: str) -> list:
    """
    :return a list of urls of all the unique album arts in the supplied playlist
    """
    urls = []
    offset = 0

    while True:
        response = sp.playlist_items(playlist, limit=100, offset=offset, fields='items(track(album(images)))')

        # reached end of list
        if len(response['items']) == 0:
            break

        # add urls
        urls += [item['track']['album']['images'][0]['url'] for item in response['items']]

        offset += len(response['items'])

    uniq_urls = list(dict.fromkeys(urls))  # remove duplicates
    logging.info(f"found {len(uniq_urls)} urls")
    return uniq_urls


def download_album_art(urls: list):
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.mkdir(DOWNLOAD_FOLDER)

    for index, url in enumerate(urls):
        r = requests.get(url, stream=True)

        if r.status_code == 200:
            r.raw.decode_content = True

            filename = f"{DOWNLOAD_FOLDER}/album-{index:02}.png"

            # write file to disk
            with open(filename, 'wb') as f_out:
                shutil.copyfileobj(r.raw, f_out)

            logging.info(f"Downloaded and saved {url} ({filename})")

        else:
            logging.warning(f"url returned non-200 response, skipping: {url}")


def generate_poster(images_path=DOWNLOAD_FOLDER, poster_width=5760, poster_height=7040, columns=9, overlay_type=None):
    img = Image.new('RGB', (poster_width, poster_height), color=0)

    album_width = poster_width // columns  # truncate to int

    path, dirs, files = next(os.walk(DOWNLOAD_FOLDER))
    images_count = len(files)

    logging.info(f"Generating poster from {images_count} images")

    # there must be a smarter way of doing this with modulo but I'm half asleep
    row = 0
    col = 0
    for image_num, image in enumerate(sorted(files)):

        logging.info(f"Inserting {images_path}/{image} at {col},{row}")

        album_art = Image.open(f"{images_path}/{image}")
        album_art.resize((album_width, album_width))

        img.paste(album_art, (col * album_width, row * album_width))

        # add overlay
        if overlay_type:
            # third arg means alpha channel is used as mask
            # https://stackoverflow.com/questions/5324647/how-to-merge-a-transparent-png-image-with-another-image-using-pil
            overlay = overlay_type(cached_average_rating[image_num], album_width)
            img.paste(overlay, (col * album_width, row * album_width), overlay)

        col += 1
        # go down to next row
        if col == columns:
            col = 0
            row += 1

    return img


def dogtag_overlay(value, album_width):
    overlay = Image.new("RGBA", (album_width, album_width), (255, 255, 255, 0))

    d = ImageDraw.Draw(overlay)

    fill_value = int((value / 10) * 255)
    mult = 0.5
    bound = 3
    text_color = int(200-(mult*fill_value) if value <= bound else (100-(mult*fill_value)))

    font = ImageFont.truetype("Familiar Pro-Bold.otf", 40)

    third = album_width / 6
    # d.polygon(((album_width-third, 0), (album_width, 0), (album_width, third)), fill=(255-fill_value, fill_value, 0))
    d.polygon(((album_width - third, 0), (album_width, 0), (album_width, third)),
              fill=(fill_value, fill_value, fill_value, 255))
    d.text((album_width - 10, 10), str(value), anchor='rt', font=font, fill=(text_color, text_color, text_color, 255))

    return overlay


def bar_overlay(value, album_width):
    overlay = Image.new("RGBA", (album_width, album_width), (255, 255, 255, 0))

    d = ImageDraw.Draw(overlay)

    fill_value = int((value / 10) * 255)

    height = 20
    # d.text((10, 10), "hello", fill=(255,255,0, 128))
    d.rectangle(((0, album_width - height), (album_width, album_width)), fill=(255 - fill_value, fill_value, 0))

    return overlay


def border_overlay(value, album_width):
    overlay = Image.new("RGBA", (album_width, album_width), (255, 255, 255, 0))

    d = ImageDraw.Draw(overlay)

    fill_value = int((value / 10) * 255)

    height = 20
    # d.text((10, 10), "hello", fill=(255,255,0, 128))
    d.rectangle((0, 0, album_width, album_width),
                fill=(0, 0, 0, 0),
                outline=(255 - fill_value, fill_value, 0, 255),
                width=10
                )

    return overlay


def greyscale_overlay(value, album_width):
    pass


def save_img(img):
    poster_filename = "out.png"
    logging.info("saving...")
    img.save(poster_filename)
    logging.info(f"saved to {poster_filename}")


def main(args: configargparse.Namespace):
    # auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    auth_manager = SpotifyOAuth(scope=SCOPE,
                                client_id=args.client_id,
                                client_secret=args.client_secret,
                                redirect_uri=args.redirect_uri)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # urls_uniq = retrieve_album_art_urls(sp, args.playlist)
    # urls_uniq = cache

    # download_album_art(urls_uniq)
    img = generate_poster(overlay_type=dogtag_overlay)
    save_img(img)
    # print(urls_uniq)


if __name__ == "__main__":
    parser = configargparse.ArgParser(default_config_files=["auth.cfg"])
    parser.add_argument("-c", "--config", is_config_file=True, help="config file path")
    parser.add_argument("--client-id", required=True, help="Spotify Client ID")
    parser.add_argument("--client-secret", required=True, help="Spotify Client Secret")
    parser.add_argument("--playlist", required=True, help="Playlist URI")
    parser.add_argument("--redirect-uri", default="http://localhost:8090", help="OAuth Redirect URI")

    args = parser.parse_args()

    main(args)
