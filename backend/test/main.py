import os
import sys
import torch


backend_folder = f"{os.getcwd()}/backend"

sys.path.append(backend_folder)


from llm.llm_model import LlmModel
from langchain_wrapper.lang_wrapper import LangWrapper


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


def main():
    gpu_numbers = select_gpu()

    try:
        devices = initialize_gpu(gpu_numbers)
        torch.FloatTensor(1).to(devices)

        model = LlmModel()
        langchain_wrapper = LangWrapper(model=model)
        generated_text = langchain_wrapper.invoke_llm_chain(
            "",
            """
            write a c++ function to interface with gpio pins of a raspberry pi. 
            GPIO0 adn GPIO1 are LEDs. Make them blink at a two seconds interval
            """,
        )
        print(generated_text)

        langchain_wrapper.cleanup()

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
