from llm.llm_model import LlmModel
from embedding.rag_wrapper import RagWrapper
from langchain.prompts import PromptTemplate
from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from langchain.chains import LLMChain, ConversationalRetrievalChain, StuffDocumentsChain
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain.chains.question_answering import load_qa_chain


# uncomment for debug
#import langchain
#langchain.debug = True  # type: ignore


class LangWrapper:
    llmModel: LlmModel | ChatOpenAI
    llmChain: LLMChain | ConversationalRetrievalChain | None
    ragWrapper: RagWrapper | None
    template_text = """Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer. 
    Keep the answer as concise as possible. 
    {context}
    Question: {question}
    Helpful Answer:"""

    def __init__(self, model: LlmModel | str):
        # initialize the LLM
        prompt = PromptTemplate.from_template(
            template=self.template_text,
        )


        if isinstance(model, LlmModel):
            self.llmModel = model
            primary_chain = LLMChain(
                prompt=prompt,
                llm=HuggingFacePipeline(pipeline=self.llmModel.pipeline),
                verbose=True,
            )
            self.llmChain = primary_chain
            self.ragWrapper = None
           


        elif model != "openai" or "mistralapi":
            print("Error: For API models, please choose openai or mistralapi")

        else:
            if model == "openai":
                self.llmModel = ChatOpenAI(model="gpt-4")
                output_parser = StrOutputParser()
                self.llmChain = prompt | self.llmModel | output_parser  # type: ignore

    def invoke_llm_chain(self, question: str):
        if self.llmChain:


            #response = self.llmChain.invoke(
            #    input={"question": question, "chat_history": self.llmChain.get_chat_history() or ""},  # type: ignore
            #)
            docs = self.ragWrapper.retriever.get_relevant_documents(question)

            response = self.llmChain({"input_documents": docs, "question": question}, return_only_outputs=True)



            if isinstance(self.llmChain, LLMChain):
                return response["output_text"]
            else:
                return response
        return "No LLM Chain instantiated in Langchain"

    # add rag if necessary
    def add_rag_wrapper(self, rag_wrapper: RagWrapper):
        self.ragWrapper = rag_wrapper

    def setup_rag_llm_chain(self):
        primary_chain = self.llmChain
        assert isinstance(primary_chain, LLMChain)
        assert isinstance(self.ragWrapper, RagWrapper)

        prompt = PromptTemplate(
            template=self.template_text,
            input_variables=["context", "question"]
        )
    
        llm=HuggingFacePipeline(pipeline=self.llmModel.pipeline)
        primary_chain = load_qa_chain(llm, chain_type="stuff", prompt=prompt)
        self.llmChain = primary_chain

    def cleanup(self):
        del self.llmChain
        if isinstance(self.llmModel, LlmModel):
            self.llmModel.cleanup()
    

