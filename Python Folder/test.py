
import torch

print("PyTorch version:", torch.__version__)

if torch.cuda.is_available():
    print("✅ PyTorch is using GPU")
    print("GPU count:", torch.cuda.device_count())
    print("GPU name:", torch.cuda.get_device_name(0))
    print("Current device index:", torch.cuda.current_device())
else:
    print("❌ PyTorch is using CPU only")


import torch
print(torch.version.cuda)
print(torch.backends.cudnn.version())

