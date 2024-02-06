import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
from typing import List
from ConcurrentDownloadManager import ConcurrentDownloadManager
import pprint

playlist_dict = {
    'RNB': [
        'https://open.spotify.com/playlist/37i9dQZF1DX7FY5ma9162x?si=d594920df161474f',
    ],
    'HipHop': [
        'https://open.spotify.com/playlist/37i9dQZF1DWY6tYEFs22tT?si=e503cb873030413a',
        'https://open.spotify.com/playlist/37i9dQZF1DX186v583rmzp?si=c33ed9096ed841b9',
    ],
}
pd.set_option('display.max_colwidth', None)


class TracksMetadataDownloader:
    def __init__(self, genre_playlist_dict: dict):
        self.sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        self.playlist_dict = genre_playlist_dict
        self.features_df = pd.DataFrame(columns=['id', 'genre'])

    def get_playlists_track_ids(self, uris: List) -> List:
        track_ids = []
        for uri in uris:
            result = self.sp.playlist(uri)['tracks']
            track_ids.extend([x['track']['id'] for x in result['items']])
            while result['next']:
                result = self.sp.next(result)
                track_ids.extend([x['track']['id'] for x in result['items']])
        return track_ids
    
    def playlist_tracks_ids_to_df(self) -> None:
        for genre, uris in self.playlist_dict.items():
            for track_id in self.get_playlists_track_ids(uris):
                self.features_df.loc[self.features_df.shape[0]] = [track_id, genre]
                
    # get audio features
    def get_tracks_audio_features(self, track_ids) -> None:
        result = self.sp.audio_features(track_ids)   
        audio_features = pd.DataFrame(result)
        audio_features.drop(['analysis_url', 'track_href', 'type', 'uri'], axis=1, inplace=True)
        self.features_df = pd.merge(self.features_df, audio_features, on="id", how="left")
        
#     # get preview urls
    def get_tracks_preview_urls(self, track_ids):
        tracks = self.sp.tracks(track_ids)['tracks']
        track_previews = [(track['id'], track['preview_url']) for track in tracks]
        previews_df = pd.DataFrame(track_previews, columns=['id', 'preview_url'])
        self.features_df = pd.merge(self.features_df, previews_df, on='id', how="left")



loader = TracksMetadataDownloader(playlist_dict)
loader.playlist_tracks_ids_to_df()
loader.get_tracks_audio_features(loader.features_df['id'].head(50).tolist())
loader.get_tracks_preview_urls(loader.features_df['id'].head(50).tolist())

loader.features_df.to_csv('dafeatures.csv')
print(loader.features_df.shape)

