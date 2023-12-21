import os
import sys
import torch

backend_folder = f"{os.getcwd()}/backend"
sys.path.append(backend_folder)


from llm.llm_model import LlmModel
from langchain_wrapper.lang_wrapper import LangWrapper

user_input = input("Enter GPU instance: ")

try:
    gpuNumber = int(user_input)
    torch.FloatTensor(1).to(f"cuda:{gpuNumber}")
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
    print("Invalid input. Please enter a valid integer.")


# Clean up
