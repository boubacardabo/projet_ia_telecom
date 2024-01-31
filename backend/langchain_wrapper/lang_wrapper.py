from llm.llm_model import LlmModel
from embedding.rag_wrapper import RagWrapper
from langchain.prompts import PromptTemplate
from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from langchain.chains import LLMChain, ConversationalRetrievalChain, StuffDocumentsChain
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser


# uncomment for debug
# import langchain
# langchain.debug = True  # type: ignore


class LangWrapper:
    llmModel: LlmModel | ChatOpenAI
    llmChain: LLMChain | ConversationalRetrievalChain
    ragWrapper: RagWrapper
    template_text = """
                    Instruction: Your job is to be be a personal coding assistant
                    that answers the questions given. Depending on this
                    instruction, the question and the context given to you, you will
                    either answer to questions related to a repository code, generate or
                    correct code. DO your BEST.
                    
                    Here is context to help:
                    {context}

                    Here is the question:
                    {question} 
                    """

    def __init__(self, model: LlmModel | str):
        # initialize the LLM
        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=self.template_text,
        )
        if isinstance(model, LlmModel):
            self.llmModel = model
            primary_chain = LLMChain(
                prompt=prompt,
                llm=HuggingFacePipeline(pipeline=self.llmModel.pipeline),
                # verbose=True,
            )
            if self.ragWrapper:
                document_prompt = PromptTemplate(
                    input_variables=["page_content"], template="{page_content}"
                )
                document_variable_name = "context"
                combine_docs_chain = StuffDocumentsChain(
                    llm_chain=primary_chain,
                    document_prompt=document_prompt,
                    document_variable_name=document_variable_name,
                )
                self.llmChain = ConversationalRetrievalChain(
                    retriever=self.ragWrapper.retriever,
                    question_generator=primary_chain,
                    combine_docs_chain=combine_docs_chain,
                    response_if_no_docs_found="The information needed was not found in any file",
                )
            else:
                self.llmChain = primary_chain
        elif model != "openai" or "mistralapi":
            print("Error: For API models, please choose openai or mistralapi")
        else:
            if model == "openai":
                self.llmModel = ChatOpenAI(model="gpt-4")
                output_parser = StrOutputParser()
                self.llmChain = prompt | self.llmModel | output_parser  # type: ignore

    def invoke_llm_chain(self, question: str):
        response = self.llmChain.invoke(input={"question": question})
        if isinstance(self.llmChain, LLMChain):
            return response["text"]
        else:
            return response

    # add rag if necessary
    def add_rag_wrapper(self, rag_wrapper: RagWrapper):
        self.ragWrapper = rag_wrapper

    def cleanup(self):
        del self.llmChain
        if isinstance(self.llmModel, LlmModel):
            self.llmModel.cleanup()
