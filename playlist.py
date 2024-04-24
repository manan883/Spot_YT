import spotipy
from spotipy.oauth2 import SpotifyOAuth
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from dotenv import load_dotenv, dotenv_values
load_dotenv()
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.environ.get('SPOTIFY_REDIRECT_URI')
# Spotify setup
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET,
                                               redirect_uri=SPOTIFY_REDIRECT_URI,
                                               scope='playlist-read-private'))
#youtube setup
YT_CLIENT_SECRET = os.environ.get('YT_CLIENT_SECRET')

def playlist(playlist_id, playlist_name_yt):
    # Get tracks from Spotify playlist
    #playlist_id = '5VNiPkohBQNeAwvae28GVt'
    results = sp.playlist(playlist_id)
    tracks = ["{} - {}".format(track['track']['name'], track['track']['artists'][0]['name']) for track in results['tracks']['items']]
    #tracks = [track['track']['name'] for track in results['tracks']['items']]
    print(tracks)
    # YouTube setup
    flow = InstalledAppFlow.from_client_secrets_file(YT_CLIENT_SECRET,
                                                    scopes=['https://www.googleapis.com/auth/youtube.force-ssl'])
    credentials = flow.run_local_server(port=0)
    youtube = build('youtube', 'v3', credentials=credentials)

    # Create YouTube playlist
    playlist_body = dict(
        snippet=dict(
            title=playlist_name_yt,
            description='Playlist created from Spotify',
            tags=['spotify', 'playlist'],
            defaultLanguage='en'
        ),
        status=dict(
            privacyStatus='private'
        )
    )

    playlists_insert_response = youtube.playlists().insert(
        part='snippet,status',
        body=playlist_body
    ).execute()

    # Add tracks to YouTube playlist
    for track in tracks:
        search_response = youtube.search().list(
            q=track,
            part='id,snippet',
            maxResults=1
        ).execute()
        
        videos = []
        for search_result in search_response.get('items', []):
            if search_result['id']['kind'] == 'youtube#video':
                videos.append(search_result['id']['videoId'])
    
        #videos = [search_result['id']['videoId'] for search_result in search_response.get('items', [])]

        if videos:
            add_video_request = youtube.playlistItems().insert(
                part='snippet',
                body={
                    'snippet': {
                        'playlistId': playlists_insert_response['id'],
                        'resourceId': {
                            'kind': 'youtube#video',
                            'videoId': videos[0]
                        }
                    }
                }
            ).execute()

#playlist('5ngjGu7rCt3gJdgxRR2q4K', 'test')
