from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from llm.model_names import dolly_model, mistral_model


class LlmModel:
    def __init__(self, model_name=mistral_model):
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            trust_remote_code=True,
        )
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.pipeline = pipeline(
            task="text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device_map="auto",
        )

    def generate_text(self, input_text: str):
        inputs = self.tokenizer.encode(
            text=input_text,
            return_tensors="pt",
        )
        output = self.model.generate(inputs)  # type: ignore
        generated_text = self.tokenizer.batch_decode(
            output, skip_special_tokens=True, device_map="auto"
        )
        return " ".join(generated_text)

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
