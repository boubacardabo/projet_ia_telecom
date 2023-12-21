import torch


def select_gpu():
    user_input = input(
        "Enter GPU instance (use comma for multiple GPUs, e.g., '0' or '0,1'): "
    )
    return user_input


def initialize_gpu(gpu_numbers):
    if torch.cuda.is_available():
        devices = f"cuda:{gpu_numbers}"
        print(f"Using GPU(s): {gpu_numbers}")
    else:
        devices = "cpu"
        print("No GPU available, using CPU.")
    return devices
