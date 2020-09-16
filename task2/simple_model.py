import torch.nn.functional as F
from torch import nn


class CNN_Net(nn.Module):

    def __init__(self, input_channels=3, output_size=1):
        super(CNN_Net, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=input_channels, out_channels=32, kernel_size=5, padding=2)
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=5, padding=2)
        self.conv3 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3)
        self.conv4 = nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3)
        self.conv5 = nn.Conv2d(in_channels=256, out_channels=428, kernel_size=3)

        self.fc1 = nn.Linear(428 * 3 * 3, 1024)  # sizes from c5
        self.fc2 = nn.Linear(1024, 128)
        self.out = nn.Linear(128, output_size)

        self.flatten_size = None

    def forward(self, x):
        c1 = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        c2 = F.max_pool2d(F.relu(self.conv2(c1)), (2, 2))
        c3 = F.max_pool2d(F.relu(self.conv3(c2)), (2, 2))
        c4 = F.max_pool2d(F.relu(self.conv4(c3)), (2, 2))
        c5 = F.max_pool2d(F.relu(self.conv5(c4)), (2, 2))

        if self.flatten_size is None:
            self.flatten_size = c5.shape[1] * c5.shape[2] * c5.shape[3]

        c5 = c5.view(-1, self.flatten_size)
        f1 = F.relu(self.fc1(c5))
        f2 = F.relu(self.fc2(f1))
        out = self.out(f2)
        return out