import spotipy

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

class Spotify(Game):
    def __init__(self, postman, output, client_id, client_secret):
        super().__init__(postman, output)
        
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = 'user-read-playback-state'
        self.redirect_uri = "https://www.google.de"

    def run(self):
        # TODO Request username from admin
        username = 'arjun-de'

        url = self.request_url(username, scope, client_id, client_secret=, redirect_uri)

        if url:
            #

        # code = Get URL that user pasted via postman and split it at '?code='
        # url.split("?code=")
        token = sp_oauth.get_access_token(code, as_dict=False)
        spotifyObject = spotipy.Spotify(auth=token)

    def connect_to_spotify(self, username) -> spotipy.Spotify:
        """ prompts the user to login if necessary and returns
            the user token suitable for use with the spotipy.Spotify
            constructor. Modified version of spotipy.prompt_user_for_token

            Parameters:
        """
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

        if not token_info:
            url = sp_oauth.get_authorize_url()
            logger.info("Please open this url in your browser: ", url)
        else:
            url = None

        return url