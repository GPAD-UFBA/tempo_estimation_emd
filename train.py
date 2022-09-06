import torch

from src.models.bpm_net import bpmNET
from src.features.upemd import UPEMD
from src.features.image_stack import ImageStack 



def train(dataloader, model, loss_fn, optimizer, device):
    size = len(dataloader.dataset)
    
    
    for batch, sample_batched  in enumerate(dataloader):
        
        X = sample_batched['audio']
        y = sample_batched['label']
        imfs = UPEMD(num_imf=6).make_imfs(X).T
        features = None
        for imf in imfs:
            imgs_stack = torch.from_numpy(ImageStack(imf, sr=11_025).create_image_stack())
            
            if features is not None:
                features = torch.stack((features,imgs_stack),dim=1)
            else:
                features = imgs_stack
        
        features, y = X.to(device), y.to(device)
        
        
        # Compute prediction error
        pred = model(X)
        loss = loss_fn(pred, y)
        
        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if batch % 100 == 0:
            loss, current = loss.item(), batch * len(X)
            print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")

def test(dataloader, model):
    size = len(dataloader.dataset)
    model.eval()
    test_loss, correct = 0, 0
    with torch.no_grad():
        for X, y in dataloader:
            X, y = X.to(device), y.to(device)
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    test_loss /= size
    correct /= size
    print(f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")


