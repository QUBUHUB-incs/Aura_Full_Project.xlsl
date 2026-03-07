import torch
import torch.nn as nn

class HybridAI(nn.Module):
    def __init__(self, in_features, hidden_dim, out_features):
        super().__init__()
        
        # 1. THE XNOR FRONT-END (Feature Extraction)
        # Maximum speed: converts complex inputs into binary patterns
        self.xnor_layer1 = XNORLinear(in_features, hidden_dim)
        self.bn1 = nn.BatchNorm1d(hidden_dim) # Keeps binary signals stable
        
        self.xnor_layer2 = XNORLinear(hidden_dim, hidden_dim)
        self.bn2 = nn.BatchNorm1d(hidden_dim)
        
        # 2. THE BOOTH BACK-END (Decision Logic)
        # High precision: Uses 8-bit Booth multiplication for the final "vote"
        self.booth_output = BoothLinear(hidden_dim, out_features, bits=8)
        
    def forward(self, x):
        # Pass through XNOR layers
        x = torch.tanh(self.bn1(self.xnor_layer1(x)))
        x = torch.tanh(self.bn2(self.xnor_layer2(x)))
        
        # Final prediction using Booth 8-bit logic
        # We scale the data to 8-bit range (-128 to 127) for the Booth layer
        x = x * 127 
        logits = self.booth_output(x)
        return logits
