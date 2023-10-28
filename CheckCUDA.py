import torch
import os

os.system('cls')

print("#####################")
print("##  CHECKING CUDA  ##")
print("#####################")

print("\nCUDA Available: ", torch.cuda.is_available())
print("CUDA Devices: ", torch.cuda.device_count())
print("CUDA Current Device: ", torch.cuda.get_device_name(torch.cuda.current_device()))