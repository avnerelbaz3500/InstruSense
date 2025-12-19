import torch
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

        # 6 blocs CNN
        self.block1 = conv_block(1, 64)
        self.pool1  = nn.MaxPool2d(2, 2)

        self.block2 = conv_block(64, 128)
        self.pool2  = nn.MaxPool2d(2, 2)

        self.block3 = conv_block(128, 256)
        self.pool3  = nn.MaxPool2d(2, 2)

        self.block4 = conv_block(256, 512)
        self.pool4  = nn.MaxPool2d(2, 2)

        self.block5 = conv_block(512, 512)
        self.pool5  = nn.MaxPool2d(2, 2)

        self.block6 = conv_block(512, 512)
        self.pool6  = nn.MaxPool2d(2, 2)

        # Fully connected head
        self.fc1 = nn.Linear(512, 1024)  # embedding size = 512 (fusion avg+max = 2*512)
        self.bn1 = nn.BatchNorm1d(1024)
        self.dropout = nn.Dropout(dropout_p)
        self.fc2 = nn.Linear(1024, n_classes)

    def forward(self, x):
        # x: (batch, 1, n_mels, n_frames)
        x = self.pool1(self.block1(x))
        x = self.pool2(self.block2(x))
        x = self.pool3(self.block3(x))
        x = self.pool4(self.block4(x))
        x = self.pool5(self.block5(x))
        x = self.pool6(self.block6(x))

        # Global max + avg pooling sur la dimension temporelle
        x_max = torch.max(x, dim=3)[0]   # shape: (batch, C, H)
        x_avg = torch.mean(x, dim=3)     # shape: (batch, C, H)
        x = x_max + x_avg                 # fusion

        # Adaptive pool pour réduire H à 1
        x = F.adaptive_avg_pool1d(x, 1).squeeze(-1)  # shape: (batch, 512)

        # Fully connected head
        x = self.fc1(x)
        x = self.bn1(x)
        x = F.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)

        return x
