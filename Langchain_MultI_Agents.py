# %% [markdown]
# Langchain supports a restricted list of opensource models. I used code llama in this case, which was one of the only models that did not ask for a meta key AND was usable without running on a GPU.

# %%


# %%
import torch
from langchain import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig, pipeline
 
torch.FloatTensor(1).to('cuda')

MODEL_NAME = "mistralai/Mistral-7B-v0.1"
#MODEL_NAME = "C:/Users/yokor/.cache/huggingface/hub/models--codellama--CodeLlama-7b-hf/snapshots/bc5283229e2fe411552f55c71657e97edf79066c"
#torch.FloatTensor(1).to('cuda')
                        
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)
 
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME
)
 
generation_config = GenerationConfig.from_pretrained(MODEL_NAME)
generation_config.max_new_tokens = 1024
generation_config.temperature = 0.0001
generation_config.top_p = 0.95
generation_config.do_sample = True
generation_config.repetition_penalty = 1.15
 
text_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    generation_config=generation_config,
)
 
llm = HuggingFacePipeline(pipeline=text_pipeline, model_kwargs={"temperature": 0})
print(llm.invoke("how many letters in the word educa?"))


# %% [markdown]
# Now we just have to invoke tools from LangChain. These tools will be used by Agents automatically, which means that the models will help choose which tool is best suited for which task.
# We can also create new tools as shown right below:

# %% [markdown]
# 

# %%
from langchain.agents import tool


@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)


tools = [get_word_length]

# %%
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are very powerful assistant, but bad at calculating lengths of words.",
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# %% [markdown]
# Now let us try using the tools provided by Langchain: You just need to bind them to our llm, so that they are used at the right time.

# %%
from langchain.tools.render import format_tool_to_openai_function

llm_with_tools = llm.bind(functions=[format_tool_to_openai_function(t) for t in tools])

# %%
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_function_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm_with_tools
    | OpenAIFunctionsAgentOutputParser()
)

# %% [markdown]
# 

# %%
#we reinvoke:
print(agent.invoke({"input": "how many letters in the word educa?", "intermediate_steps": []}))



# %%
#For a more complex example, we can reiterate over the same agent:
from langchain.schema.agent import AgentFinish

user_input = "how many letters in the word educa?"
intermediate_steps = []
while True:
    output = agent.invoke(
        {
            "input": user_input,
            "intermediate_steps": intermediate_steps,
        }
    )
    if isinstance(output, AgentFinish):
        final_result = output.return_values["output"]
        break
    else:
        print(f"TOOL NAME: {output.tool}")
        print(f"TOOL INPUT: {output.tool_input}")
        tool = {"get_word_length": get_word_length}[output.tool]
        observation = tool.run(output.tool_input)
        intermediate_steps.append((output, observation))
print(final_result)

# %%
#Using AgentExecutor, we can have the same code with a simpler interface:
from langchain.agents import AgentExecutor

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

print(agent_executor.invoke({"input": "how many letters in the word educa?"}))



# %%
#Here we add some memory:
from langchain.prompts import MessagesPlaceholder

MEMORY_KEY = "chat_history"
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are very powerful assistant, but bad at calculating lengths of words.",
        ),
        MessagesPlaceholder(variable_name=MEMORY_KEY),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# %%
from langchain.schema.messages import AIMessage, HumanMessage

chat_history = []

# %%
agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_function_messages(
            x["intermediate_steps"]
        ),
        "chat_history": lambda x: x["chat_history"],
    }
    | prompt
    | llm_with_tools
    | OpenAIFunctionsAgentOutputParser()
)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# %%
input1 = "how many letters in the word educa?"
result = agent_executor.invoke({"input": input1, "chat_history": chat_history})
chat_history.extend(
    [
        HumanMessage(content=input1),
        AIMessage(content=result["output"]),
    ]
)
print(agent_executor.invoke({"input": "is that a real word?", "chat_history": chat_history}))


