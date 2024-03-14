import pandas as pd
import numpy as np
from collections import defaultdict
import librosa
from ConcurrentDownloadManager import ConcurrentDownloadManager

class AudioFeatureExtraction:
    def __init__(self, data_df):
        self.data_df = data_df
    
    def _extract_mfcc_mean(self, audio_series, sample_rate):
        mfcc = np.array(librosa.feature.mfcc(y=audio_series, sr=sample_rate, n_mfcc= 13))
        return mfcc.mean(axis=1)
    
    def _extract_chroma_mean(self, audio_series, sample_rate):
        chroma = np.array(librosa.feature.chroma_stft(y=audio_series, sr=sample_rate, n_chroma=12))
        return chroma.mean(axis=1)
    
    def extract_audio_features(self):
        audio_features_dict = defaultdict(list)

        for _, entry in self.data_df.iterrows():
            audio_features_dict['id'].append(entry['id'])

            audio_series, sample_rate = librosa.load(f"songs/{entry['id']}.mp3", offset=0, duration=30)
            for i, val in enumerate(self._extract_mfcc_mean(audio_series, sample_rate)):
                audio_features_dict[f"mfcc_{i+1}Mean"].append(val)
            print("Finished MFCC extraction")

            for i, val in enumerate(self._extract_chroma_mean(audio_series, sample_rate)):
                audio_features_dict[f"chroma_{i+1}Mean"].append(val)
            print("Finished Chroma extraction")



        return pd.DataFrame(audio_features_dict)
    
data_df = pd.read_csv("data/filtered_music_data.csv")

print("Starting Audio Extraction...")

audio_feature_extractor = AudioFeatureExtraction(data_df)
audio_features_df = audio_feature_extractor.extract_audio_features()

print("Finished Audio Extraction!")

merged_df = pd.merge(data_df, audio_features_df, on='id')
merged_df.to_csv("data/filtered_music_data_with_librosa.csv", index=False)

