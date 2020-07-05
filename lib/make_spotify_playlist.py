'''
@author Calvin Huang
@date 2020-7-2

Tubify: Youtube to Spotify

create_spotify_playlist.py
'''
import json
import requests
from secrets import spotify_uid, oauth_token

class CreateSpotifyPlaylist:

    def __init__(self):
        self.user_id = spotify_uid

    def get_youtube_client(self):
        pass

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
        response_json = response.json()

        return response_json['id']

    def find_spotify_song(self):
        pass

    def transfer_song(self):
        pass
