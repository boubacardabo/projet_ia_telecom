from llm.llm_model import LlmModel
from embedding.rag_wrapper import RagWrapper
from langchain.prompts import PromptTemplate
from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from langchain.chains import LLMChain, ConversationalRetrievalChain, StuffDocumentsChain
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationSummaryBufferMemory, ConversationBufferWindowMemory

# uncomment for debug
# import langchain
# langchain.debug = True  # type: ignore


class LangWrapper:
    llmModel: LlmModel
    llmChain: LLMChain | ConversationalRetrievalChain | None
    pipeline: HuggingFacePipeline
    someMemory: list[tuple]
    memory: ConversationSummaryBufferMemory | None
    ragWrapper: RagWrapper | None
    prompt : PromptTemplate
    

    def __init__(self, llmModel: LlmModel, prompt=prompt_template_RAG):
        self.prompt = prompt
        llm_instance = llmModel.model if llmModel.is_open_llm else HuggingFacePipeline(pipeline=llmModel.pipeline)
        
        # initialize the LLM
        prompt = PromptTemplate.from_template(self.template_text)
        if isinstance(model, LlmModel):
            self.llmModel = model
            self.pipeline = HuggingFacePipeline(pipeline=self.llmModel.pipeline)
            primary_chain = LLMChain(
                prompt=prompt,
                llm=self.pipeline,
                verbose=True,
            )
            self.llmChain = primary_chain
            self.someMemory = []
            self.ragWrapper = None
            self.memory = None

        elif model != "openai" or "mistralapi":
            print("Error: For API models, please choose openai or mistralapi")
        else:
            if model == "openai":
                self.llmModel = ChatOpenAI(model="gpt-4")
                output_parser = StrOutputParser()
                self.llmChain = prompt | self.llmModel | output_parser  # type: ignore

    
    # add rag if necessary
    def add_rag_wrapper(self, rag_wrapper: RagWrapper):
        self.ragWrapper = rag_wrapper

    def setup_rag_llm_chain(self):
        primary_chain = self.llmChain
        assert isinstance(primary_chain, LLMChain)
        assert isinstance(self.ragWrapper, RagWrapper)

        self.memory = ConversationSummaryBufferMemory(llm=self.pipeline, max_token_limit=30)

        document_prompt = PromptTemplate(
            input_variables=["page_content", "file_name", "file_path", "source"], 
            template="""
            The file {file_name} has this content: 
            {page_content}

            Here are the metadata of the file
            file_path={file_path}, source={source}
            """
        )

        combine_docs_chain = StuffDocumentsChain(
            llm_chain=primary_chain,
            document_prompt=document_prompt,
            document_variable_name='context',
        )

        self.llmChain = ConversationalRetrievalChain(
            retriever=self.ragWrapper.retriever,
            question_generator=primary_chain,
            combine_docs_chain=combine_docs_chain,
            response_if_no_docs_found="The information needed was not found in any file",
        )

        

    def invoke_llm_chain(self, question: str, includeHist: bool= False):
        if self.llmChain:
            # "chat_history": [self.someMemory[-1]]
            response = self.llmChain(
                    {'question': question, "chat_history":"", "histo":""},  # type: ignore
            )
            self.memory.save_context({"input": question}, {"output": response['answer']})
            print(self.memory.load_memory_variables({}))
            return response
            
        return "No LLM Chain instantiated in Langchain"




    def setup_rag_llm_chain2(self):

        """ An alternative RAG chain setup"""

        primary_chain = self.llmChain
        assert isinstance(primary_chain, LLMChain)
        assert isinstance(self.ragWrapper, RagWrapper)

        from langchain.chains.question_answering import load_qa_chain
        
        prompt = PromptTemplate.from_template(template=self.template_text)
        
        self.llmChain = load_qa_chain(self.llmModel, chain_type="stuff", prompt=prompt)


    def invoke_llm_chain2(self, question: str):
        """ An alternative RAG chain"""
        if self.llmChain:

            docs = self.ragWrapper.retriever.get_relevant_documents(question)
            response = self.llmChain.invoke({"input_documents": docs, "question": question}, return_only_outputs=True)

            return response
        return "No LLM Chain instantiated in Langchain"
    


    def invoke_llm_chain3(self, function, specification):
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
