from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from llm.model_names import mistral_model
from utils.utils import select_gpu_if_available
from langchain_community.llms import OpenLLM


class LlmModel:
    is_open_llm: bool
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, model_name=mistral_model, is_open_llm=False):

        self.is_open_llm = is_open_llm

        if is_open_llm:
            self.model = OpenLLM(model_id=model_name)

        else:
            dtype = select_gpu_if_available()
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_name, trust_remote_code=True, use_fast=False
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=dtype,
                device_map="auto",
            )

            self.pipeline = pipeline(
                task="text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device_map="auto",
                max_new_tokens=1000,
                return_full_text=False,
            )

    def generate_text(self, input_text: str):
        if self.is_open_llm:
            return self.model.invoke(input_text)
        else:
            inputs = self.tokenizer.encode(
                text=input_text,
                return_tensors="pt",
            )

            output = self.model.generate(inputs)

            generated_text = self.tokenizer.batch_decode(
                output, skip_special_tokens=True, device_map="auto"
            )
            return " ".join(generated_text)

    def cleanup(self):

        if not self.is_open_llm:
            del self.tokenizer

        # Delete references to the model
        del self.model

        # Empty gpu cache
        from torch.cuda import empty_cache

        empty_cache()

        # Perform garbage collection to release memory
        from gc import collect

        collect()
