import pandas as pd
from TracksMetadataDownloader import TracksMetadataDownloader
from ConcurrentDownloadManager import ConcurrentDownloadManager
from AudioFeatureExtraction import AudioFeatureExtraction

# Fetch spotify dataset
print("Fetching Spotify dataset...")
playlist_genre_table_df = pd.read_csv('data/spotify_playlists_source.csv')
playlist_genre_dict = {}
for key, value in playlist_genre_table_df.groupby('Genre')['Playlist URL']:
    playlist_genre_dict[key] = value.tolist()

loader = TracksMetadataDownloader(playlist_genre_dict)
loader.playlist_tracks_ids_to_df()
loader.get_tracks_metadata()

# Download 30-second song snippets
print("Downloading 30-second snippets...")
data_df_wo_prevs = loader.features_df.dropna(subset=["preview_url"])
data_df_wo_prevs.reset_index(drop=True, inplace=True)

downloads_manager = ConcurrentDownloadManager()
downloads_manager.downloadFiles([(f"songs/{entry['id']}.mp3", entry['preview_url']) for _, entry in data_df_wo_prevs.iterrows()])

# Extract Librosa audio features
print("Starting Audio Extraction...")

audio_feature_extractor = AudioFeatureExtraction(data_df_wo_prevs)
audio_features_df = audio_feature_extractor.extract_audio_features()

merged_df = pd.merge(loader.features_df, audio_features_df, on='id', how='left')

# Export raw dataset with spotify and librosa features
merged_df.to_csv("data/raw_dataset.csv", index=False)
print("Exported raw dataset!")