import os
from langchain_huggingface import HuggingFaceEndpoint
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.tools import DuckDuckGoSearchResults
from langchain.agents import initialize_agent, AgentType
from langchain_core.prompts import PromptTemplate
from langchain.tools import Tool

# 🚀 Setting Hugging Face API Token
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

# 🎯 Initializing LLM Model from Hugging Face
llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-72B-Instruct",  # AI Model
    task="text-generation",
    max_new_tokens=512,
    do_sample=False,
    repetition_penalty=1.03,
)

# 🔍 Loading DuckDuckGo Search Tool
wrapper = DuckDuckGoSearchAPIWrapper(time="d",)
search_tool = DuckDuckGoSearchResults(api_wrapper=wrapper,)

# 🔧 Defining the Search Tool for the Agent
search = Tool(
    name="DuckDuckGo Search",
    func=search_tool.invoke,
    description="Use this tool to search the latest news from DuckDuckGo."
)

tools = [search]

# 📝 Defining Prompt Template for the Agent
template = '''You are an intelligent assistant with access to the following tools:

{tools}

When given a question, follow this format:

Question: {input}

Thought: Consider whether you need to use a tool.

Action: the action to take, choose one from [{tool_names}]

Action Input: the input for the action

Observation: the result of the action

Thought: Now you can provide the final answer.

Final Answer: the final answer to the original question.

Begin!

Question: {input}
'''

prompt = PromptTemplate.from_template(template)

# 🤖 Initializing AI Agent
agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    prompt=prompt,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=6,
    stop_sequence="Final Answer:"
)

# 📢 Getting User Query
query = input("❓ Enter your question: ")

# 🎯 Running the Agent to Get a Response
response = agent_executor.run(query)
print("\n🧠 Final Answer: ", response)
