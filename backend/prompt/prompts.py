from langchain.prompts import PromptTemplate, ChatPromptTemplate



prompt1 = ChatPromptTemplate.from_messages([
    ("system", """[INST] You are a helpful code assistant that help with writing Python code for a user requests.
                """),

    ("user", """You will be given a function, and a unit test specification for the function. Your task is to write the implementation of the unit test such that it passes all requirements in the specification.
                """),

    ("user", " here is the function : \n ------------\n {input_function} \n ------------\n"),

    ("user", "here is the specification of the unit test : \n ------------\n {input_specification} \n ------------\n "),

    ("system", """Make sure to generate all test cases. Please output EXACTLY the python CODE in Markdown format, e.g.:

    ```python
    ....
    ```
    and NOTHING else. [/INST]""")
    ])
    


prompt_usecase_test_system = PromptTemplate.from_template(
"""
You'll be given an object to test by the user. This object could be a class or a function. The user might also give you the name of a relevant file. Your goal is to write a system or unit test of that object. Use the PyTest module. Make sure to properly import all the necessary modules. Your final answer must be your code. Be concise, answer the request as best you can. You have access to the following tool:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question


Begin!

Question: {input}
Thought:{agent_scratchpad}
"""
)
