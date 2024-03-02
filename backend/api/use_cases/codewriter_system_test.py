
from langchain_wrapper.lang_wrapper import LangWrapper
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import AgentExecutor, create_react_agent
from prompt.prompts import prompt_usecase_test_system


def invoke_agent(lang_wrapper: LangWrapper, question: str):

        retriever = lang_wrapper.ragWrapper.retriever

        retriever_tool = create_retriever_tool(
            retriever,
            "RAG-search",
            """This is a RAG tool to search relevant information about the object before writing a system test for it. To use it, the action input should follow the following template : 
            <name of the file> | <name of the function or class>.
            """
        )

        tools = [retriever_tool]

        # Get the prompt to use
        prompt = prompt_usecase_test_system

        llm = lang_wrapper.llm_instance

        # Construct the ReAct agent
        agent = create_react_agent(llm, tools, prompt)

        # Create an agent executor by passing in the agent and tools
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

        generated_output = agent_executor.invoke({"input": question})

        return generated_output["output"]




