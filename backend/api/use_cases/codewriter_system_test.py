from langchain_wrapper.lang_wrapper import LangWrapper
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import AgentExecutor, create_react_agent
from prompt.prompts import prompt_usecase_test_system
from llm.llm_model import LlmModel
from embedding.rag_wrapper import RagWrapper


def setup_agent(
    model: LlmModel, has_rag: bool, repo_url=None, branch=None, file_type=None
):
    lang_wrapper = None
    use_case_object = None
    if not has_rag:
        raise Exception("RAG needs to be enabled for this use case")
    else:
        assert repo_url
        assert file_type
        ragWrapper = RagWrapper(repo_url=repo_url, branch=branch, file_type=file_type)
        lang_wrapper = LangWrapper(llmModel=model)
        lang_wrapper.add_rag_wrapper(ragWrapper)
        lang_wrapper.setup_rag_llm_chain()

        retriever = lang_wrapper.ragWrapper.retriever  # type: ignore

        retriever_tool = create_retriever_tool(
            retriever,
            "RAG-search",
            """This is a RAG tool to search relevant information about the object before writing a system test for it. To use it, the action input should follow the following template : 
            <name of the file> | <name of the function or class>.
            """,
        )

        tools = [retriever_tool]

        # Get the prompt to use
        prompt = prompt_usecase_test_system

        llm = lang_wrapper.llm_instance

        # Construct the ReAct agent
        agent = create_react_agent(llm, tools, prompt)

        # Create an agent executor by passing in the agent and tools
        agent_executor = AgentExecutor(
            agent=agent, tools=tools, verbose=True, handle_parsing_errors=True  # type: ignore
        )
        use_case_object = agent_executor

    return use_case_object


def invoke_agent(agent_executor: AgentExecutor, question: str):

    generated_output = agent_executor.invoke({"input": question})
    return generated_output["output"]
