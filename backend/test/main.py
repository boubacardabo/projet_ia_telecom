import os
import sys
import torch


backend_folder = f"{os.getcwd()}/backend"

sys.path.append(backend_folder)


from llm.llm_model import LlmModel
from langchain_wrapper.lang_wrapper import LangWrapper
from llm.model_names import mistral_model, orca_2_model


def select_gpu():
    user_input = input(
        "Enter GPU instance (use comma for multiple GPUs, e.g., '0' or '0,1'): "
    )
    gpu_numbers = [int(gpu.strip()) for gpu in user_input.split(",")]
    return gpu_numbers


def initialize_gpu(gpu_numbers):
    if torch.cuda.is_available():
        devices = [f"cuda:{gpu}" for gpu in gpu_numbers]
        print(f"Using GPU(s): {', '.join(map(str, gpu_numbers))}")
    else:
        devices = ["cpu"]
        print("No GPU available, using CPU.")

    return devices


def main():
    gpu_numbers = select_gpu()

    try:
        devices = initialize_gpu(gpu_numbers)
        for device in devices:
            torch.FloatTensor(1).to(device)

        model = LlmModel(model_name=orca_2_model)
        langchain_wrapper = LangWrapper(model=model)
        context = ""
        question = """
            write a python function to interface with gpio pins of a raspberry pi. 
            GPIO0 adn GPIO1 are LEDs. Make them blink at a two seconds interval
            """
        # generated_text = langchain_wrapper.invoke_llm_chain(context, question)
        gen_text = model.generate_text(question)
        print(gen_text)

        langchain_wrapper.cleanup()

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
