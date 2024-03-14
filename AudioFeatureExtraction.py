import pandas as pd
import numpy as np
import librosa
from ConcurrentDownloadManager import ConcurrentDownloadManager

class AudioFeatureExtraction:
    def __init__(self, data_df):
        self.data_df = data_df
    
    def _extract_mfcc_mean(self, audio_series, sample_rate):
        mfcc = np.array(librosa.feature.mfcc(audio_series, sample_rate))
        return mfcc.mean(axis=1)
    
    def _extract_spect_mean(self, audio_series, sample_rate):
        spect = np.array(librosa.feature.melspectrogram(audio_series, sample_rate))
        return spect.mean(axis=1)
    
    def _extract_chroma_mean(self, audio_series, sample_rate):
        chroma = np.array(librosa.feature.chroma_stft(audio_series, sample_rate))
        return chroma.mean(axis=1)
    
    def _extract_centroid_mean(self, audio_series, sample_rate):
        centroid = np.array(librosa.feature.tonnetz(audio_series, sample_rate))
        return centroid.mean(axis=1)
    
    def extract_audio_features(self):
        audio_features_dict = {
            'id': [],
            'mfcc_mean': [],
            'spect_mean': [],
            'chroma_mean': [],
            'centroid_mean': []
        }
        for _, entry in self.data_df.iterrows():
            audio_features_dict['id'].append(entry['id'])

            audio_series, sample_rate = librosa.load(f"songs/{entry['id']}.mp3", offset=0, duration=30)
            audio_features_dict['mfcc_mean'].append(self._extract_mfcc_mean(audio_series, sample_rate))
            audio_features_dict['spect_mean'].append(self._extract_spect_mean(audio_series, sample_rate))
            audio_features_dict['chroma_mean'].append(self._extract_chroma_mean(audio_series, sample_rate))
            audio_features_dict['centroid_mean'].append(self._extract_centroid_mean(audio_series, sample_rate))

        return pd.DataFrame(audio_features_dict)
    
data_df = pd.read_csv("data/filtered_music_data.csv")

downloads_manager = ConcurrentDownloadManager()
downloads_manager.downloadFiles([(f"songs/{entry['id']}.mp3", entry['preview_url']) for _, entry in data_df.iterrows()])

audio_feature_extractor = AudioFeatureExtraction(data_df)
audio_features_df = audio_feature_extractor.extract_audio_features()

merged_df = pd.merge(data_df, audio_features_df, on='id')
merged_df.to_csv("data/filtered_music_data_with_librosa")

