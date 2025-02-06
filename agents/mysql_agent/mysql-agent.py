import pymysql
pymysql.install_as_MySQLdb()

from langchain_huggingface import HuggingFaceEndpoint
import os
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents import initialize_agent
from langchain.agents import AgentType

# Set Hugging Face API token
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

# Initialize LLM model with HuggingFaceEndpoint
llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-72B-Instruct",
    task="text-generation",
    max_new_tokens=512,
    do_sample=False,
    repetition_penalty=1.03,
)

# Connect to MySQL database (Replace with your MySQL credentials)
engine = create_engine('mysql://root:Meysam1386@localhost:3306/smartHub')

# Create an SQLDatabase object for MySQL connection
db = SQLDatabase(engine)

# Configure database tools for the agent
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()

# Initialize Agent with HuggingFace
agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # Using an appropriate agent type
    verbose=True
)

# Example query input
example_query = "What phones are there to buy?"

# Execute the agent and print the response
response = agent_executor.run(example_query)
print(response)
