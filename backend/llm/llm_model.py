from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from llm.model_names import mistral_model
from utils.utils import select_gpu_if_available

model_name = mistral_model

class LlmModel:
    def __init__(self, model_name=model_name, llm_runnable=False):

        if not llm_runnable : 
            dtype = select_gpu_if_available()

            self.tokenizer = AutoTokenizer.from_pretrained(
                model_name, trust_remote_code=True, use_fast=False
            )

            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=dtype,
                # device_map= "auto",
            )
            #print("model tensor device:", self.model.device)

            self.pipeline = pipeline(
                task="text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0,
                max_new_tokens=4096,
                return_full_text=False,
            )

            #print("pipeline tensor device:", self.pipeline.device)
        else: 

            server_url = "http://localhost:3000"
            from langchain_community.llms import OpenLLM
            self.llm = OpenLLM(server_url=server_url)

    def generate_text(self, input_text: str):

        if not self.llm :
            inputs = self.tokenizer.encode(
                text=input_text,
                return_tensors="pt",
            )
            #print("Input tensor device:", inputs.device)

            output = self.model.generate(inputs)  # type: ignore

            #print("Output tensor device:", output.device)


            generated_text = self.tokenizer.batch_decode(
                output, skip_special_tokens=True, device_map="auto"
            )
            return " ".join(generated_text)

        else : 
            return self.llm.invoke(input_text)

    def cleanup(self):

        if not self.llm :
            # If you're using a GPU, make sure to release GPU memory
            if self.model.device.type == "cuda":  # type: ignore

                self.model = self.model.to("cpu")  # Move model to CPU to release GPU memory
                #import torch
                

            # Delete references to the model
            del self.model
            del self.tokenizer
        
        else : 

            del self.llm
            import torch
            torch.cuda.empty_cache()
        # Perform garbage collection to release memory
        import gc
        gc.collect()
