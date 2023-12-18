from transformers import AutoTokenizer, AutoModelForCausalLM
from llm.model_names import opt_350_model
import torch


class LlmModel:
    def __init__(self, model_name=opt_350_model):
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name, trust_remote_code=True
        )
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    def generate_text(self, input_text: str):
        inputs = self.tokenizer.encode(input_text, return_tensors="pt")
        print(inputs)
        output = self.model.generate(inputs)  # type: ignore
        generated_text = self.tokenizer.decode(output, skip_special_tokens=True)[0]
        return generated_text

    def cleanup(self):
        # Ensure any open files or connections are properly closed
        # For transformers, this might include closing the model's tokenizer
        self.tokenizer.clean_up_tokenization_spaces()

        # If you're using a GPU, make sure to release GPU memory
        if self.model.device.type == "cuda":  # type: ignore
            self.model = self.model.to("cpu")  # Move model to CPU to release GPU memory

        # Delete references to the model
        del self.model
        del self.tokenizer

        # Perform garbage collection to release memory
        import gc

        gc.collect()
