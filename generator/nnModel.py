"""
Train on the data
"""
import math
import time
import torch
import torch.nn as nn
from torch.autograd import Variable

from .helpers import *

class CharRNN(nn.Module):
    """
    We use GRU as I heard that it take less time to train
    """
    def __init__(self, input_size, hidden_size, output_size, n_layers=1):
        super(CharRNN, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.n_layers = n_layers

        self.encoder = nn.Embedding(input_size, hidden_size)
        self.rnn = nn.GRU(hidden_size, hidden_size, n_layers)

        self.decoder = nn.Linear(hidden_size, output_size)

    def forward(self, input_var, hidden):
        batch_size = input_var.size(0)
        encoded = self.encoder(input_var)
        output, hidden = self.rnn(encoded.view(1, batch_size, -1), hidden)
        output = self.decoder(output.view(batch_size, -1))
        return output, hidden

    def forward2(self, input_var, hidden):
        encoded = self.encoder(input_var.view(1, -1))
        output, hidden = self.rnn(encoded.view(1, 1, -1), hidden)
        output = self.decoder(output.view(1,-1))
        return output, hidden

    def init_hidden(self, batch_size):
        return Variable(torch.zeros(self.n_layers, batch_size,
                                    self.hidden_size))
