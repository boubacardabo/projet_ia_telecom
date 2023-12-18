from transformers import AutoTokenizer, AutoModelForCausalLM, LlamaTokenizer
from llm.model_names import dolly_model, mistral_model
import torch


class LlmModel:
    def __init__(self, model_name=mistral_model):
        self.tokenizer = LlamaTokenizer.from_pretrained(
            model_name, trust_remote_code=True
        )
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    def generate_text(self, input_text: str):
        inputs = self.tokenizer.encode(
            text=input_text,
            return_tensors="pt",
            add_special_tokens=False,
        )
        output = self.model.generate(inputs, max_new_tokens=2000)  # type: ignore
        generated_text = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return generated_text

    def cleanup(self):
        # If you're using a GPU, make sure to release GPU memory
        if self.model.device.type == "cuda":  # type: ignore
            self.model = self.model.to("cpu")  # Move model to CPU to release GPU memory

        # Delete references to the model
        del self.model
        del self.tokenizer

        # Perform garbage collection to release memory
        import gc

        gc.collect()
