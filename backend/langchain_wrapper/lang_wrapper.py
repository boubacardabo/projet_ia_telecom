from llm.llm_model import LlmModel
from langchain.prompts import PromptTemplate
from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser


# uncomment for debug
langchain.debug = True  # type: ignore


class LangWrapper:
    llmModel: LlmModel | ChatOpenAI
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

    def __init__(self, model: LlmModel | str):
        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=self.template_text,
        )
        if isinstance(model, LlmModel):
            self.llmModel = model
            self.llmChain = LLMChain(
                prompt=prompt,
                llm=HuggingFacePipeline(pipeline=self.llmModel.pipeline),
                # verbose=True,
            )
        elif model != "openai" or "mistralapi":
            print("Error: For API models, please choose openai or mistralapi")
        else:
            if model == "openai":
                self.llmModel = ChatOpenAI(model="gpt-4")
                output_parser = StrOutputParser()
                self.llmChain = prompt | self.llmModel | output_parser  # type: ignore

    def invoke_llm_chain(self, context, question: str):
        response = self.llmChain.invoke(
            input={"context": context, "question": question}
        )
        if isinstance(self.llmChain, LLMChain):
            return response["text"]
        else:
            return response

    def cleanup(self):
        del self.llmChain
        if self.llmModel is LlmModel:
            self.llmModel.cleanup()
