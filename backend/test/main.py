import os
import sys
import torch


backend_folder = f"{os.getcwd()}/backend"

sys.path.append(backend_folder)


from llm.llm_model import LlmModel
from langchain_wrapper.lang_wrapper import LangWrapper
from llm.model_names import mistral_model, orca_2_model


def main():
    try:
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
