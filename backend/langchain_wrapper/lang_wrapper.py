from llm.llm_model import LlmModel
from embedding.rag_wrapper import RagWrapper
from langchain.prompts import PromptTemplate
from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from langchain.chains import LLMChain, ConversationalRetrievalChain, StuffDocumentsChain
from langchain.memory import ConversationBufferWindowMemory
from prompt.prompts import prompt_template_RAG

# uncomment for debug
# import langchain
# langchain.debug = True  # type: ignore


class LangWrapper:
    llmModel: LlmModel
    llmChain: LLMChain | ConversationalRetrievalChain | None
    memory: ConversationBufferWindowMemory | None
    ragWrapper: RagWrapper | None
    prompt: PromptTemplate

    def __init__(self, llmModel: LlmModel, prompt=prompt_template_RAG):
        self.prompt = prompt
        llm_instance = (
            llmModel.model
            if llmModel.is_open_llm
            else HuggingFacePipeline(pipeline=llmModel.pipeline)
        )

        # initialize the LLM
        self.llmModel = llmModel
        if not llmModel.is_open_llm :
            self.pipeline = HuggingFacePipeline(pipeline=self.llmModel.pipeline)

        primary_chain = LLMChain(
            prompt=prompt,
            llm=llm_instance,
            #verbose=True,
        )
        self.llmChain = primary_chain
        self.ragWrapper = None
        self.memory = None

    # add rag if necessary
    def add_rag_wrapper(self, rag_wrapper: RagWrapper):
        self.ragWrapper = rag_wrapper

    def setup_rag_llm_chain(self):
        primary_chain = self.llmChain
        assert isinstance(primary_chain, LLMChain)
        assert isinstance(self.ragWrapper, RagWrapper)

        self.memory = ConversationBufferWindowMemory(k=1)

        document_prompt = PromptTemplate(
            input_variables=["page_content", "file_name", "file_path", "source"],
            template="""
            The file {file_name} has this content: 
            {page_content}

            Here are the metadata of the file
            file_path={file_path}, source={source}
            """,
        )

        combine_docs_chain = StuffDocumentsChain(
            llm_chain=primary_chain,
            document_prompt=document_prompt,
            document_variable_name="context",
        )

        self.llmChain = ConversationalRetrievalChain(
            retriever=self.ragWrapper.retriever,
            question_generator=primary_chain,
            combine_docs_chain=combine_docs_chain,
            response_if_no_docs_found="The information needed was not found in any file",
        )

    # Be sure to check your prompt template variables and pass them in
    def invoke_llm_chain(self, **kwargs):
        invoke_params = (
            {
                **kwargs,
                "histo": self.memory.load_memory_variables({})["history"],
                "chat_history": "",
            }
            if self.memory
            else {**kwargs}
        )

        if self.llmChain:
            response = self.llmChain(invoke_params)
            if self.memory == None:
                return response["text"]
            else:
                self.memory.save_context(
                    {"input": kwargs.get("question")}, {"output": response["answer"]}
                )
                return response["answer"]                

        return "No LLM Chain instantiated in Langchain"
    


    def invoke_llm_chain_code_writer_unit_test_usecase(self, function, specification):
        """For the 'code writer' usecase"""
        if self.llmChain:

            response = self.llmChain.invoke(
                input={"input_function": function, "input_specification": specification}

            )
            if isinstance(self.llmChain, LLMChain):
                return response["text"]
            else:
                return response
        return "No LLM Chain instantiated in Langchain"


    def cleanup(self):
        del self.llmChain
        if isinstance(self.llmModel, LlmModel):
            self.llmModel.cleanup()
