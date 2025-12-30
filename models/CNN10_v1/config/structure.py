'''
import torch.nn as nn
import torch.nn.functional as F


class Model(nn.Module):

    def __init__(self, n_classes, dropout_p=0.5):
        super().__init__()

        def conv_block(in_ch, out_ch):
            return nn.Sequential(
                nn.Conv2d(in_ch, out_ch, kernel_size=3, padding=1),
                nn.BatchNorm2d(out_ch),
                nn.ReLU(),
            )

        # 3 blocs CNN (comme dans le checkpoint)
        self.block1 = conv_block(1, 64)
        self.pool1 = nn.MaxPool2d(2, 2)

        self.block2 = conv_block(64, 128)
        self.pool2 = nn.MaxPool2d(2, 2)

        self.block3 = conv_block(128, 256)
        self.pool3 = nn.MaxPool2d(2, 2)

        # Une seule couche fully connected (comme dans le checkpoint)
        self.fc = nn.Linear(256, n_classes)

    def forward(self, x):
        # x: (batch, 1, n_mels, n_frames)
        x = self.pool1(self.block1(x))
        x = self.pool2(self.block2(x))
        x = self.pool3(self.block3(x))

        # Global average pooling
        x = F.adaptive_avg_pool2d(x, 1)  # shape: (batch, 256, 1, 1)
        x = x.view(x.size(0), -1)  # shape: (batch, 256)

        # Fully connected
        x = self.fc(x)

        return x
'''
import torch
import torch.nn as nn
import torch.nn.functional as F


class Model(nn.Module):
    def __init__(self, n_classes, dropout_p=0.3):
        super().__init__()
        def conv_block(in_ch, out_ch):
            return nn.Sequential(
                nn.Conv2d(in_ch, out_ch, kernel_size=3, padding=1),
                nn.BatchNorm2d(out_ch),
                nn.ReLU(),
            )

        self.block1 = conv_block(1, 64)
        self.pool1  = nn.MaxPool2d(2, 2)

        self.block2 = conv_block(64, 128)
        self.pool2  = nn.MaxPool2d(2, 2)

        self.block3 = conv_block(128, 256)
        self.pool3  = nn.MaxPool2d(2, 2)

        # Fully connected head
        self.fc1 = nn.Linear(256, 512)
        self.bn1 = nn.BatchNorm1d(512)
        self.dropout = nn.Dropout(dropout_p)
        self.fc2 = nn.Linear(512, n_classes)

    def forward(self, x):
        x = self.pool1(self.block1(x))
        x = self.pool2(self.block2(x))
        x = self.pool3(self.block3(x))

        x_max = torch.max(x, dim=3)[0]
        x_avg = torch.mean(x, dim=3)
        x = x_max + x_avg

        x = F.adaptive_avg_pool1d(x, 1).squeeze(-1)
        x = self.fc1(x)
        x = self.bn1(x)
        x = F.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)

        return x