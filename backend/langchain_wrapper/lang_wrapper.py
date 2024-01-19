from llm.llm_model import LlmModel
from langchain.prompts import PromptTemplate
from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import GitLoader
import langchain
import os
from git import Repo

# uncomment for debug
# langchain.debug = True  # type: ignore


class LangWrapper:
    llmModel: LlmModel | ChatOpenAI
    llmChain: LLMChain
    repo_local_path: str
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

    def __init__(self, model: LlmModel | str, repo_url: str, branch: str | None = None):
        # Initialize the repo vectorstore we will use
        self.downloadRepository(repo_url)
        self.loadRepositoryDocs(branch=branch)
        # initialize the LLM
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

    def loadRepositoryDocs(self, branch: str | None = None):
        try:
            loader = GitLoader(
                repo_path=self.repo_local_path,
                # file_filter=lambda file_path: file_path.endswith(".py"),
                branch=branch or "main",
            )
            docs = loader.load()

        except Exception as e:
            print(e)

    def downloadRepository(
        self,
        repo_url: str,
    ):
        repo_name = repo_url.split("/")[-1]
        if repo_name.endswith(".git"):
            repo_name = repo_name[:-4]

        local_path = os.path.join("remote_code", repo_name)
        if not os.path.isdir(local_path):
            print("Cloning repository")
            try:
                repo = Repo.clone_from(
                    url=repo_url,
                    to_path=local_path,
                    no_checkout=True,
                )
                print("Repository was successfully cloned")
            except Exception as e:
                print(e)
        else:
            print("Repository already exists")
        self.repo_local_path = local_path

    def cleanup(self):
        del self.llmChain
        if isinstance(self.llmModel, LlmModel):
            self.llmModel.cleanup()
