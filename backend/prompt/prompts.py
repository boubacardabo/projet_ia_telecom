from langchain.prompts import PromptTemplate, ChatPromptTemplate, ChatMessagePromptTemplate
#from mistralai.models.chat_completion import ChatMessage
from langchain_mistralai.chat_models import ChatMessage


prompt1 = ChatPromptTemplate.from_messages([
    ("system", """[INST] You are a helpful code assistant that help with writing Python code for a user requests.
                """),

    ("user", """You will be given a function, and a unit test specification for the function. Your task is to write the implementation of the unit test such that it passes all requirements in the specification.
                """),

    ("user", " here is the function : \n ------------ {input_function} \n ------------"),

    ("user", "here is the specification of the unit test : \n ------------ {input_specification} \n ------------ "),

    ("system", """Please output EXACTLY the python CODE, and make sure to generate all test cases. Make sure to end the python code with "```". [/INST]""")
    
    
    ])
    


prompt_mixtral = ChatPromptTemplate.from_messages([

    ChatMessage(role="user", content="You will be given a function, and a unit test specification for the function. Your task is to write the implementation of the function such that it passes all requirements in the specification."),

    ChatMessage(role="assistant", content="Please provide the function."),

    ChatMessage(role="user", content="{input_function}"),

    ChatMessage(role="assistant", content="Thank you. Now, please provide the unit test specification."),

    ChatMessage(role="user", content="{input_specification}")
    
])
#prompt mixtral doesn't work because {...} don't get replaced

