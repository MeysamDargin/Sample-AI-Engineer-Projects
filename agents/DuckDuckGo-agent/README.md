# Intelligent Assistant using LangChain and Hugging Face

This Python script integrates various tools to create an intelligent assistant capable of answering questions and performing searches using LangChain, Hugging Face, and DuckDuckGo. It utilizes the `Qwen/Qwen2.5-72B-Instruct` model from Hugging Face for text generation, along with the DuckDuckGo search API to provide real-time search results.

## Requirements

- Python 3.x
- Install the required Python libraries:

```bash
pip install langchain huggingface_hub langchain_community duckduckgo-search
```

## Setup

Before running the script, you'll need to set up the following:

### Hugging Face API Token

You must set your Hugging Face API token in the environment variable `HUGGINGFACEHUB_API_TOKEN`. This token is required to access the Hugging Face model.

You can get your API token from [Hugging Face's website](https://huggingface.co/settings/tokens).

To set the environment variable:

```bash
export HUGGINGFACEHUB_API_TOKEN="your_huggingface_token_here"
```

### DuckDuckGo API

The script uses the DuckDuckGo search tool. The DuckDuckGo API is already integrated into the code, so no additional setup is required for this API.

## Script Overview

The script initializes an AI agent using the following components:

- **Hugging Face Model**: A text-generation model (`Qwen/Qwen2.5-72B-Instruct`) is used to process the input question and generate a response.
- **DuckDuckGo Search**: This tool allows the agent to perform real-time web searches using DuckDuckGo. This is especially useful when the AI model needs to gather additional information for answering the question.
- **LangChain**: LangChain is used to manage the tools, agents, and prompt templates. The agent is set up to take a question from the user and decide whether it needs to use the DuckDuckGo search tool or just generate a response using the model.

## How to Run

1. Clone or download this repository.
2. Install the required dependencies.
3. Set your Hugging Face API token as described in the setup section.
4. Run the script:

```bash
python DuckDuckGo-search.py
```
## Dependencies
Refer to `requirements.txt` for a full list of dependencies.

Follow the steps below to set up and run the project:
```sh
pip install -r requirements.txt
```
5. When prompted, enter your question. The AI will process it and return the final answer.

## Example Usage

```
❓ Enter your question: What is the latest news about AI?
```

The AI will use the DuckDuckGo search tool to gather the latest news on AI, and the response will be displayed as:

```
🧠 Final Answer: [Latest news results]
```

## Customization

- **Model**: You can replace the model by specifying a different Hugging Face model in the `repo_id`.
- **Search Tool**: If you prefer a different search tool, you can replace the DuckDuckGo search implementation with another API or custom search logic.

## Contributing

Feel free to open issues or pull requests to improve the functionality, fix bugs, or add new features to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
