import requests
from bs4 import BeautifulSoup
import random
import asyncio
import os
import nest_asyncio
from langchain.agents import AgentType, initialize_agent
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import create_async_playwright_browser
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from langchain.tools import Tool

nest_asyncio.apply()

# Function to search on Bing
def search_bing(query):
    headers = {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        ])
    }
    url = f"https://www.bing.com/search?q={query.replace(' ', '+')}"
    response = requests.get(url, headers=headers)
    return response.text if response.status_code == 200 else None

# Function to parse search results
def parse_results(html):
    soup = BeautifulSoup(html, "html.parser")
    results = []
    for result in soup.find_all("li", class_="b_algo"):
        try:
            title_tag = result.find("h2")
            link_tag = title_tag.find("a") if title_tag else None
            snippet_tag = result.find("p")
            if title_tag and link_tag:
                title = title_tag.text.strip()
                link = link_tag["href"]
                snippet = snippet_tag.text.strip() if snippet_tag else "No description"
                results.append({"title": title, "link": link, "snippet": snippet})
        except Exception as e:
            print(f"Error processing result: {e}")
    return results

# Initialize Playwright browser
async_browser = create_async_playwright_browser()
toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)
playwright_tools = toolkit.get_tools()  # Retrieve Playwright tools

# Set up language model (LLM)
os.environ["HUGGINGFACEHUB_API_TOKEN"] = ""
llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-72B-Instruct",
    task="text-generation",
    max_new_tokens=512,
    do_sample=False,
    repetition_penalty=1.03,
)

# Prompt template for the agent
search_prompt_template = PromptTemplate(
    input_variables=["query", "results"],
    template=""" 
You are an intelligent assistant responsible for providing the most accurate and relevant answer based on the user's query. Search results are retrieved based on the requested language, and you may use other languages if necessary.

Step 1: Analyze the user's query and transform it into a structured question for Bing search.

User query: "{query}"

Step 2: Retrieve and review Bing search results. Consider only the most relevant ones.

Bing search results: {results}

Your task:
- Review the search results and identify the most relevant URL.
- Extract relevant information from the selected website.
- If needed, refine or cross-check the information with other links.
- Perform only the requested tasks.
- Provide the final answer concisely and accurately.
"""
)

# Create Bing Search tool for the agent
class BingSearchTool(Tool):
    def __init__(self):
        super().__init__(name="BingSearch", func=self.arun, description="Search on Bing for relevant results.")

    async def arun(self, query, verbose=False, **kwargs):
        if verbose:
            print(f"Searching on Bing for: {query}")
        results = search_bing(query)
        if not results:
            return "No results found."

        # Check if callbacks are correctly passed
        if 'callbacks' in kwargs and isinstance(kwargs['callbacks'], list):
            callbacks = kwargs['callbacks']
            for callback in callbacks:
                callback('Processing search results...')
        
        return parse_results(results)

# Initialize agent with Bing search tools
bing_search_tool = BingSearchTool()
tools = [bing_search_tool] + playwright_tools

# Configure agent without verbose mode
agent_chain = initialize_agent(
    tools,  # Agent tools
    llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Function to process user requests
async def process_user_request(user_query):
    print("\n⏳ Agent is processing the request...\n")
    
    # Perform Bing search
    bing_results = await bing_search_tool.arun(user_query)
    
    if isinstance(bing_results, str):
        print(bing_results)  # If no results are found
        return

    # Format results for the prompt
    formatted_results = "\n".join([f"{i+1}. {res['title']} - {res['link']}" for i, res in enumerate(bing_results)])
    
    # Create prompt for the agent
    decision_prompt = search_prompt_template.format(query=user_query, results=formatted_results)

    print("🎯 Agent is analyzing search results...\n")
    
    # Run the agent
    response = await agent_chain.arun(decision_prompt)
    
    # Display final response
    print("\n💡 Agent Response:\n", response)

# Main execution
async def main():
    user_input = input("🔍 Please enter your query: ")
    await process_user_request(user_input)

asyncio.run(main())