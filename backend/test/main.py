import os
import sys
import torch


backend_folder = f"{os.getcwd()}/backend"
sys.path.append(backend_folder)


from llm.llm_model import LlmModel
from langchain_wrapper.lang_wrapper import LangWrapper
from utils.main import select_gpu, initialize_gpu


def main():
    gpu_numbers = select_gpu()

    try:
        devices = initialize_gpu(gpu_numbers)
        torch.FloatTensor(2).to("cuda")

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

    except ValueError:
        print("Invalid input. Please enter valid GPU instance(s).")


if __name__ == "__main__":
    main()
