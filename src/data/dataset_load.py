import torch
import librosa
from torch.utils.data import Dataset
import os
import glob
import pandas as pd
from random import shuffle
import numpy as np



class CustomAudioDataset(Dataset):
    
    
    def __init__(self, annotations_file, audio_dir,transform, sample_rate = 11_025):
        self.audio_labels = pd.read_csv(annotations_file)
        self.audio_dir = audio_dir
        self.files = glob.glob(audio_dir + '\*.wav')
        self.data_tuples = []
        self.sample_rate = sample_rate
        self.transform = transform
        
        
    def get_audio(self,idx):
        data, label = self.load_audio(self.files[idx])
        padded_audio = self.pad_audio(data)
        return padded_audio, np.array(label)
    
                
    def load_audio(self, audio_path):
            audio_file = os.path.splitext(os.path.basename(audio_path))[0]
            data, _ = librosa.load(audio_path,sr=self.sample_rate)
            label = self.audio_labels.loc[self.audio_labels['File'] == audio_file]['Tempo'].values[0]
            return data, label
    
    def pad_audio(self, data):
        if data.shape[0] < 30*self.sample_rate:
            zeros = torch.zeros(30*self.sample_rate - data.shape[0], data.shape[1]).double()
            data = torch.cat((data, zeros), axis=0)
            
        data = data[:30*self.sample_rate]
        return data
    
        
    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        
        if torch.is_tensor(idx):
            idx = idx.tolist()
        
        
        audio, label = self.get_audio(idx)
        # sample = torch.from_numpy(sample)
        
        if self.transform:
            audio, label = self.transform( (audio, label))

        return {'audio': audio, 'label': label}
    
class ToTensor(object):
    """Convert ndarrays in sample to Tensors."""

    def __call__(self, sample):
        audio, label = sample[0], sample[1]

        # swap color axis because
        # numpy image: H x W x C
        # torch image: C x H x W
        
        return torch.from_numpy(audio),torch.from_numpy(label)
