import torch
from torch.utils.data import DataLoader
from torch.utils.data import random_split
import torch.nn as nn


from src.models.bpm_net import bpmNET
from src.data.dataset_load import CustomAudioDataset, ToTensor
from train import train, test

if __name__ == '__main__':
    src_mirum = CustomAudioDataset(annotations_file='bpms_database\SMC_MIRUM.csv',
                                audio_dir='dataset\smc_mirum_tempo',
                                transform=ToTensor())
    

    print(len(src_mirum))
    train_size = int(len(src_mirum)*0.7)
    test_size = len(src_mirum) - train_size

    train_data, test_data = random_split(src_mirum, [train_size, test_size])
    print("The length of train data is:",len(train_data))
    print("The length of test data is:",len(test_data))

    train_dataloader = DataLoader(train_data, batch_size=2, shuffle=True)
    test_dataloader = DataLoader(test_data, batch_size=2, shuffle=True)
    
    model = bpmNET()
    loss_fn = nn.CrossEntropyLoss()
    learning_rate = 1e-3
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Using {} device".format(device))
    epochs = 15
    for t in range(epochs):
        print(f"Epoch {t+1}\n-------------------------------")
        train(train_dataloader, model, loss_fn, optimizer, device)
        test(test_dataloader, model)
    print("Done!")
        
    
    

    
