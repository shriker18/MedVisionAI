import torch

tensor = torch.tensor([
    [0, 128, 255],
    [64, 192, 32]
])

print(tensor)
print("Shape:", tensor.shape)
print("Data type:", tensor.dtype)
