import spotipy
import requests
import io
from PIL import Image
import numpy as np

from table.games.Game import Game
from table.Postman import Topics
from table.utils.Commands import CMD

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class Spotify(Game):
    def __init__(self, postman, output, config_handler):
        super().__init__(postman, output)

        self.config_handler = config_handler
        self.client_id = config_handler.get_value("Spotify", "client_id")
        self.client_secret = config_handler.get_value("Spotify", "client_secret")
        self.scope = 'user-modify-playback-state user-read-playback-state'
        self.redirect_uri = "https://www.google.de"
        self.spotifyObject = None

    def start(self):
        self.output.empty_matrix()

        self.spotifyObject = self.connect_to_spotify()

        self.postman.send(Topics.OUTPUT, "I am connected to Spotify now. Let's listen to some "
                                         "awesome tunes. 🎵")

        self.running = True
        while self.running:
            self.print_cover()
            self.read_user_input()

    def connect_to_spotify(self) -> spotipy.Spotify:
        """ Connects to spotiy and prompts user for authorization if necessary.

            Returns:
                Authorized Spotify object to access spotify API.
        """
        username = self.config_handler.get_value("Spotify", "username")

        if username:
            self.postman.send(Topics.OUTPUT, f"I am using the last used Spotify username ({username}).")
            #TODO "To connect to another account send `account` "

        else:
            # Request username
            self.postman.send(Topics.OUTPUT, "Please send me your Spotify user name.")

            # Wait until username is received
            post = None
            while not post:
                post = self.postman.request(Topics.INPUT)
            username = post['message']

            self.config_handler.set_value("Spotify", "username", username)

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
            self.postman.send(Topics.OUTPUT, "Then send me the complete url you are redirected to.")

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

        if track is not None:
            try:
                cover_art_url = track['item']['album']['images'][0]['url']
            except TypeError:
                # Sometime the API returns a NoneType when changing the track
                # Just waiting for the next iterations is fine.
                logger.debug("TypeError when retrieving album url.")
                return

            i = requests.get(cover_art_url)
            img = Image.open(io.BytesIO(i.content)).convert("RGB")
            img = img.resize((12, 12), Image.ANTIALIAS)

            self.output.pixel_matrix = np.array(img)
            self.output.show()

    def read_user_input(self):
        post = self.postman.request(Topics.INPUT)
        while post:
            cmd = post['message']
            if cmd == CMD.RIGHT:
                self.spotifyObject.next_track()
            elif cmd == CMD.LEFT:
                self.spotifyObject.previous_track()
            elif cmd == CMD.X:
                current_track = self.spotifyObject.current_user_playing_track()
                if current_track["is_playing"]:
                    self.spotifyObject.pause_playback()
                else:
                    self.spotifyObject.start_playback()
            elif cmd == CMD.START:
                self.running = False
                break

            # Check if there is even more to read
            post = self.postman.request(Topics.INPUT)

    def draw_icon(self, output):
        super().draw_icon(output)

        file = np.load("spotify_logo.npz")
        output.pixel_matrix[1:11, 1:11] = file["spotify_logo"][1:11, 1:11]
        output.show()
