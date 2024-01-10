from llm.llm_model import LlmModel
from langchain.prompts import PromptTemplate
from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from langchain.chains import LLMChain
import langchain

# uncomment for debug
langchain.debug = True  # type: ignore


class LangWrapper:
    llmModel: LlmModel
    llmChain: LLMChain
    template_text = """
                    Instruction: Your job is to be write or correct code depending 
                    on this instruction, the question and the context given to you.
                    Do your BEST to write CORRECT CODE. Do not include any test results
                    or comments. As an output only give me the code requested
                    
                    Here is context to help:
                    {context}

                    ### QUESTION:
                    {question} 
                    """

    def __init__(self, model: LlmModel):
        self.llmModel = model
        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=self.template_text,
        )

        self.llmChain = LLMChain(
            prompt=prompt,
            llm=HuggingFacePipeline(pipeline=self.llmModel.pipeline),
            verbose=True,
        )

    def invoke_llm_chain(self, context, question: str):
        return self.llmChain.invoke(input={"context": context, "question": question})[
            "text"
        ]

    def cleanup(self):
        del self.llmChain
        self.llmModel.cleanup()
