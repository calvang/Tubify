'''
@author Calvin Huang
@date 2020-07-02

Tubify: Youtube to Spotify

make_spotify_playlist.py
'''
import os
import json
import requests
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from secrets import spotify_uid, oauth_token

class MakeSpotifyPlaylist:

    def __init__(self):
        self.user_id = spotify_uid
        self.token = oauth_token
        self.youtube_client = get_youtube_client()

    def get_youtube_client(self):
        '''Retrieves client from Youtube API'''
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "youtube_client_secrets.json"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()
        client = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)
        return client

    def get_youtube_playlist(self):
        pass

    def create_spotify_playlist(self,playlist):
        '''Send POST to Spotify API'''
        request_body = json.dumps({
            'name': '',
            'description': playlist,
            'public': True
        })
        url = 'https://api.spotify.com/v1/users/{}/playlists'.format(self.user_id)
        response = requests.post(
            url,
            data = request_body,
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(oauth_token)
            }
        )
        response = response.json()

        return response['id']

    def find_spotify_song(self, song_name, artist):
        '''Send GET request for a song'''
        url = 'https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit-20'.format(
            song_name,
            artist
        )
        response = requests.get(
            url,
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(oauth_token)
            }
        )
        response = response.json()
        songs = response['tracks']['items']

        return songs[0]

    def transfer_song(self):
        pass
