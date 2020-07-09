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
import youtube_dl
from secrets import spotify_uid, oauth_token

class MakeSpotifyPlaylist:

    def __init__(self):
        '''Initialize variables'''
        self.user_id = spotify_uid
        self.token = oauth_token
        self.youtube_client = get_youtube_client()
        self.songs_dict = {}

    def get_youtube_client(self):
        '''Retrieve client from Youtube API'''
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

    def get_youtube_playlist(self, youtube_playlist_name):
        '''Retrieve playlist, then videos from playlist'''
        playlist_request = self.youtube_client.list(
            part='snippet,contentDetails,statistics'
        )
        playlist_response = playlist_request.execute()

        playlist = {
            'id': '',
            'name': '',
            'videos': []
        }
        for item in playlist_response['items']:
            title = item['snippet']['title']
            if title == youtube_playlist_name:
                playlist['name'] = title
                playlist['id'] = item['id']
                break;

        videos_request = self.youtube_client.videos().list(
            part='snippet,contentDetails,statistics',
            playlistId = playlist['id']
        )
        videos_response = videos_request.execute()


        for item in videos_response['items']:
            vid_title = item['snippet']['title']
            youtube_url = 'https://www.youtube.com/watch?v={}'.format(item['id'])
            video = youtube_dl.YoutubeDL({}).extract_innfo(youtube_url, download=False)
            song_name = video['track']
            song_artist = video['artist']
            spotify_uri = self.find_spotify_song(song_name, song_artist)
            self.songs_dict[vid_title] = {
                'youtube_url': youtube_url,
                'song_name': song_name,
                'song_artist': song_artist,
                'spotify_uri': spotify_uri
            }


    def create_spotify_playlist(self, playlist_name, playlist_desc):
        '''Send POST to Spotify API'''
        request_body = json.dumps({
            'name': playlist_name,
            'description': playlist_desc,
            'public': True
        })
        url = 'https://api.spotify.com/v1/users/{}/playlists'.format(self.user_id)
        response = requests.post(
            url,
            data = request_body,
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(self.token)
            }
        )
        response = response.json()

        return response['id']

    def find_spotify_song(self, song_name, song_artist):
        '''Send GET request for a song'''
        url = 'https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit-20'.format(
            song_name,
            song_artist
        )
        response = requests.get(
            url,
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(self.token)
            }
        )
        response = response.json()
        songs = response['tracks']['items']
        uri = songs[0]

        return uri

    def transfer_songs(self, youtube_playlist, spotify_playlist_name):
        '''Place all songs into Spotify playlist'''
        self.get_youtube_playlist(self, youtube_playlist)
        
        song_uris = [data['spotify_uri'] for song, data in self.songs_dict.items()]
        playlist_id = self.create_spotify_playlist(spotify_playlist_name)
        url = 'https://api.spotify.com/v1/playlists/{}/tracks'.format(playlist_id)
        json_data = json.dumps(song_uris)

        response = requests.post(
            url,
            data = json_data,
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(self.token)
            }
        )