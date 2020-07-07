'''
@author Calvin Huang
@date 2020-07-02

Tubify: Youtube to Spotify

make_spotify_playlist.py
'''
import json
import requests
from secrets import spotify_uid, oauth_token

class MakeSpotifyPlaylist:

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
        response = response.json()

        return response['id']

    def find_spotify_song(self, song_name, artist):
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
