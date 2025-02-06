# MySQL LangChain Agent

This project integrates LangChain with a MySQL database, utilizing Hugging Face's LLM models to interact with the database and generate intelligent responses.

## Features
- Uses **LangChain** to create an intelligent agent.
- Connects to a **MySQL** database using `SQLAlchemy`.
- Utilizes a **Hugging Face** model for text generation.
- Implements **SQLDatabaseToolkit** to manage database queries.

## Installation
To set up the project, install the required dependencies:

```sh
pip install -r requirements.txt
```

## Configuration
1. Update the MySQL connection string in the script:
   ```python
   engine = create_engine('mysql://username:password@localhost:3306/database_name')
   ```
2. Set the **Hugging Face API token**:
   ```sh
   export HUGGINGFACEHUB_API_TOKEN='your_api_token'
   ```

## Usage
Run the script to execute the LangChain agent:

```sh
python mysql-agent.py
```

Modify `example_query` in the script to customize the database query.

## Dependencies
Refer to `requirements.txt` for a full list of dependencies.

Follow the steps below to set up and run the project:
```sh
pip install -r requirements.txt
```

## License
This project is licensed under the MIT License.

