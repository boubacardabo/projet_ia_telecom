from langchain.prompts import PromptTemplate, ChatPromptTemplate

prompt1 = prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful code assistant that help with writing Python code for a user requests. Output EXACTLY the PYTHON CODE.
                """),

    ("user", """You will be given a function, and a unit test specification for the function. Your task is to write the implementation of the function such that it passes all requirements in the specification.
                """),

    ("ai", "Please provide the function."),

    ("user", "{input_function}"),

    ("ai", "Thank you. Now, please provide the unit test specification."),

    ("user", "{input_specification}")
    
])