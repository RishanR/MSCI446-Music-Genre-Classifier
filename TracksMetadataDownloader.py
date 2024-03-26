import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth
from typing import List

pd.set_option('display.max_colwidth', None)


class TracksMetadataDownloader:
    def __init__(self, genre_playlist_dict: dict):
        scope = "user-library-read"
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
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
        return audio_features
        # self.features_df = pd.merge(self.features_df, audio_features, on="id", how="left")
    
    def get_tracks_artist_genres(self, tracks):
        artist_genres = []
        for track in tracks:
            id = track['id']
            artists = self.sp.artists([artist['id'] for artist in track['artists']])['artists']
            genres = [genre for artist in artists for genre in artist['genres']]
            genres = list(set(genres))
            artist_genres.append((id, genres))
        artist_genres_df = pd.DataFrame(artist_genres, columns=['id', 'artist_genre'])
        return artist_genres_df

#     # get preview urls
    def get_tracks_preview_urls(self, tracks):
        track_previews = [(track['id'], track['preview_url']) for track in tracks]
        previews_df = pd.DataFrame(track_previews, columns=['id', 'preview_url'])
        return previews_df
        # self.features_df = pd.merge(self.features_df, previews_df, on='id', how="left")

    def get_tracks_metadata(self):
        limit = 50
        audio_features = pd.DataFrame()
        artist_genres = pd.DataFrame()
        preview_urls = pd.DataFrame()

        partitions = [self.features_df[i:i+limit] for i in range(0, self.features_df.shape[0], limit)]
        for tracks in partitions:
            tracks_info = self.sp.tracks(tracks['id'].tolist())['tracks']
            audio_features = pd.concat([audio_features, self.get_tracks_audio_features(tracks['id'].tolist())])
            artist_genres = pd.concat([artist_genres, self.get_tracks_artist_genres(tracks_info)])
            preview_urls = pd.concat([preview_urls, self.get_tracks_preview_urls(tracks_info)])
        self.features_df = pd.merge(self.features_df, audio_features, on="id", how="left")
        self.features_df = pd.merge(self.features_df, artist_genres, on="id", how="left")
        self.features_df = pd.merge(self.features_df, preview_urls, on="id", how="left")