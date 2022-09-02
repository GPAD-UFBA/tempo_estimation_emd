import torch
import librosa
from torch.utils.data import Dataset
import os
import glob
import pandas as pd
from random import shuffle

class CustomAudioDataset(Dataset):
    
    
    def __init__(self, annotations_file, audio_dir,transform, window_size, stride, sample_rate = 16_000):
        self.audio_labels = pd.read_csv(annotations_file)
        
        self.audio_dir = audio_dir
        self.files = glob.glob(audio_dir + '\*.wav')
        self.window_size = window_size
        self.stride = stride
        self.data_tuples = []
        self.sample_rate = sample_rate
        self.transform = transform

        self.create_data_tuples()
        
        
        
    def create_data_tuples(self):
        for audio_path in self.files:
            data, label = self.load_audio(audio_path)
            padded_audio = self.pad_audio(data)
            
            idxs = [i for i in range(0, padded_audio.size(0) - self.window_size, self.stride)]
            if len(idxs) == 0:
                continue
            
            self.create_index_tuples(idxs, audio_path, label)
            
        shuffle(self.data_tuples)

                
    def load_audio(self, audio_path):
            audio_file = os.path.splitext(os.path.basename(audio_path))[0]
            data, _ = librosa.load(audio_path,sr=self.sample_rate)
            data = torch.from_numpy(data)            
            label = self.audio_labels.loc[self.audio_labels['File'] == audio_file]['Tempo'].values[0]
            return data, label
    
    def pad_audio(self, data):
        if data.size(0) % self.window_size != 0:
            zeros = torch.zeros(abs(self.window_size - (data.size(0) % self.window_size)), data.size(1)).double()
            data = torch.cat((data, zeros), axis=0)
        return data
    
    def create_index_tuples(self,idxs,audio_path,label):
        for j in idxs:
            data_tuple = (audio_path, j, label)
            self.data_tuples.append(data_tuple)
        
    def __len__(self):
        return len(self.data_tuples)

    def __getitem__(self, idx):
        
        if torch.is_tensor(idx):
            idx = idx.tolist()
            
        sample_tuple = self.data_tuples[idx]
        sample, _ = librosa.load(sample_tuple[0],sr=self.sample_rate)
        sample = torch.from_numpy(sample)
        label = sample_tuple[2]
        sample = sample[sample_tuple[1]: sample_tuple[1] + self.window_size]

        if self.transform:
            sample = self.transform(sample)

        return {'sample': sample, 'label': label}
    