import torch

torch.FloatTensor(1).to("cuda")
import sys

# sys.path.append("/Users/boubacardabo/Desktop/school/projet_ia_telecom/backend")
sys.path.append("/Users/boubacardabo/Desktop/school/projet_ia_telecom/backend")

from llm.llm_model import LlmModel

llm = LlmModel()
generated_text = llm.generate_text("Hello,")
print("Generated text:", generated_text)

# Clean up
llm.cleanup()
