import pandas as pd
import numpy as np
from collections import defaultdict
import librosa

class AudioFeatureExtraction:
    def __init__(self, data_df):
        self.data_df = data_df
    
    def _extract_mfcc(self, audio_series, sample_rate):
        mfcc = np.array(librosa.feature.mfcc(y=audio_series, sr=sample_rate, n_mfcc=13))
        return (mfcc.mean(axis=1), mfcc.std(axis=1))
    
    def _extract_chroma(self, audio_series, sample_rate):
        chroma = np.array(librosa.feature.chroma_stft(y=audio_series, sr=sample_rate, n_chroma=12))
        return (chroma.mean(axis=1), chroma.std(axis=1))
    
    def _extract_tonal(self, audio_series, sample_rate):
        tonal = np.array(librosa.feature.tonnetz(y=audio_series, sr=sample_rate))
        return (tonal.mean(axis=1), tonal.std(axis=1))
    
    def _extract_zero_cross(self, audio_series):
        zero_cross = np.array(librosa.feature.zero_crossing_rate(y=audio_series))
        return (zero_cross.mean(), zero_cross.std())
    
    def _extract_spect_centroid(self, audio_series, sample_rate):
        spect_centroid = np.array(librosa.feature.spectral_centroid(y=audio_series, sr=sample_rate))
        return (spect_centroid.mean(), spect_centroid.std())
    
    def _extract_spect_contrast(self, audio_series, sample_rate):
        spect_contrast = np.array(librosa.feature.spectral_contrast(y=audio_series, sr=sample_rate))
        return (spect_contrast.mean(), spect_contrast.std()) 
    
    def _extract_spect_bw(self, audio_series, sample_rate):
        spect_bw = np.array(librosa.feature.spectral_bandwidth(y=audio_series, sr=sample_rate))
        return (spect_bw.mean(), spect_bw.std())
    
    def _extract_spect_rolloff(self, audio_series, sample_rate):
        spect_rolloff = np.array(librosa.feature.spectral_rolloff(y=audio_series, sr=sample_rate))
        return (spect_rolloff.mean(), spect_rolloff.std())
    
    def extract_audio_features(self):
        audio_features_dict = defaultdict(list)

        for i, entry in self.data_df.iterrows():
            audio_features_dict['id'].append(entry['id'])
            print(f"Extracting Audio Features: {i+1}/{self.data_df.shape[0]}")
            audio_series, sample_rate = librosa.load(f"songs/{entry['id']}.mp3", offset=0, duration=30)
            
            mfcc_mean, mfcc_std = self._extract_mfcc(audio_series, sample_rate)
            for i in range(len(mfcc_mean)):
                audio_features_dict[f"mfcc_{i+1}Mean"].append(mfcc_mean[i])
                audio_features_dict[f"mfcc_{i+1}Std"].append(mfcc_std[i])

            chroma_mean, chroma_std = self._extract_chroma(audio_series, sample_rate)
            for i in range(len(chroma_mean)):
                audio_features_dict[f"chroma_{i+1}Mean"].append(chroma_mean[i])
                audio_features_dict[f"chroma_{i+1}Std"].append(chroma_std[i])

            tonal_mean, tonal_std = self._extract_tonal(audio_series, sample_rate)
            for i in range(len(tonal_mean)):
                audio_features_dict[f"tonal_{i+1}Mean"].append(tonal_mean[i])
                audio_features_dict[f"tonal_{i+1}Std"].append(tonal_std[i])
            
            zero_val = self._extract_zero_cross(audio_series)
            audio_features_dict[f"zero_cross_Mean"].append(zero_val[0])
            audio_features_dict[f"zero_cross_Std"].append(zero_val[1])

            cent_val = self._extract_spect_centroid(audio_series, sample_rate)
            audio_features_dict[f"spect_centroid_Mean"].append(cent_val[0])
            audio_features_dict[f"spect_centroid_Std"].append(cent_val[1])

            cont_val = self._extract_spect_contrast(audio_series, sample_rate)
            audio_features_dict[f"spect_contrast_Mean"].append(cont_val[0])
            audio_features_dict[f"spect_contrast_Std"].append(cont_val[1])

            bw_val = self._extract_spect_bw(audio_series, sample_rate)
            audio_features_dict[f"spect_bw_Mean"].append(bw_val[0])
            audio_features_dict[f"spect_bw_Std"].append(bw_val[1])

            rolloff_val = self._extract_spect_rolloff(audio_series, sample_rate)
            audio_features_dict[f"spect_rolloff_Mean"].append(rolloff_val[0])
            audio_features_dict[f"spect_rolloff_Std"].append(rolloff_val[1])

        return pd.DataFrame(audio_features_dict)
    
data_df = pd.read_csv("data/filtered_music_data.csv")

print("Starting Audio Extraction...")

audio_feature_extractor = AudioFeatureExtraction(data_df)
audio_features_df = audio_feature_extractor.extract_audio_features()

print("Finished Audio Extraction!")

merged_df = pd.merge(data_df, audio_features_df, on='id')
merged_df.to_csv("data/filtered_music_data_with_librosa_v2.csv", index=False)

