import spotipy
import requests
import io
from PIL import Image
import numpy as np
import json

from table.games.Game import Game
from table.Postman import Topics

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class Spotify(Game):
    def __init__(self, postman, output):
        super().__init__(postman, output)

        with open('config.json') as config_file:
            config = json.load(config_file)

        self.client_id = config["spotify_client_id"]
        self.client_secret = config["spotify_client_secret"]
        self.scope = 'user-read-playback-state'
        self.redirect_uri = "https://www.google.de"
        self.spotifyObject = None

    def start(self):
        self.spotifyObject = self.connect_to_spotify()

        while True:
            self.print_cover()

    def connect_to_spotify(self) -> spotipy.Spotify:
        """ Connects to spotiy and prompts user for authorization if necessary.

            Returns:
                Authorized Spotify object to access spotify API.
        """
        # Request username
        self.postman.send(Topics.OUTPUT, "Please send me your Spotify user name.")

        # Wait until username is received
        post = None
        while not post:
            post = self.postman.request(Topics.INPUT)
        username = post['message']

        cache_path = ".cache-" + username
        sp_oauth = spotipy.SpotifyOAuth(
            self.client_id,
            self.client_secret,
            self.redirect_uri,
            scope=self.scope,
            cache_path=cache_path,
            show_dialog=False
        )

        # try to get a valid token for this user, from the cache,
        # if not in the cache, the create a new (this will send
        # the user to a web page where they can authorize this app)
        token_info = sp_oauth.get_cached_token()

        if token_info:
            token = token_info["access_token"]
        else:
            logger.debug("No cached spotify token found. Requesting authorization.")
            url = sp_oauth.get_authorize_url()
            self.postman.send(Topics.OUTPUT, f"Please open this url in your browser: {url}")

            # Wait for return url
            post = None
            while not post:
                post = self.postman.request(Topics.INPUT)

            url = post['message']
            code = url.split("?code=")[-1]

            token = sp_oauth.get_access_token(code, as_dict=False)

        return spotipy.Spotify(auth=token)

    def print_cover(self):
        track = self.spotifyObject.current_user_playing_track()

        if track is None:
            logger.debug("No track is playing.")
            return

        cover_art_url = track['item']['album']['images'][0]['url']

        i = requests.get(cover_art_url)
        img = Image.open(io.BytesIO(i.content)).convert("RGB")
        img = img.resize((12, 12), Image.ANTIALIAS)

        self.output.pixel_matrix = np.array(img)
        self.output.show()

    def draw_icon(self, output):
        super().draw_icon(output)

        file = np.load("spotify_logo.npz")
        output.pixel_matrix[1:11, 1:11] = file["spotify_logo"][1:11, 1:11]
        output.show()
