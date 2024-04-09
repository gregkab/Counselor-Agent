# Counselor Agent

## Project Overview

This project demonstrates how to build a simple API server using FastAPI to interface with the OpenAI API. It serves as a backend for a Streamlit frontend client that requests essays based on user input. The application aims to evolve into a counselor agent, providing academic and counseling support to students at universities.

## Environment Setup

1. **Install Anaconda or Miniconda**: Ensure you have Anaconda or Miniconda installed on your machine. If not, download and install from [Anaconda](https://www.anaconda.com/products/individual) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

2. **Create a Conda Environment**: Open your terminal and run the following command to create a new Conda environment named `langchain-demo` with Python 10.

   ```bash
   conda create --name langchain-demo python=10
   ```

3. **Activate the Environment**: Activate the newly created environment using:

   ```bash
   conda activate langchain-demo
   ```

4. **Install Requirements**: Navigate to the project directory and install the required packages using:

   ```bash
   pip install -r requirements.txt
   ```

5. **Environment Variables**: Copy `.env.example` to a new file named `.env` and fill in the required API keys.

   ```bash
   cp .env.example .env
   ```

## Running the Application

1. **Start the FastAPI Server**: Run the following command to start the FastAPI server in api folder.

   ```bash
   uvicorn api.main:app --reload
   ```

2. **Launch the Streamlit Client**: In a new terminal window, ensure the `counselor-agent` environment is activated and run:

   ```bash
   streamlit run client.py
   ```

3. **Use the Application**: Navigate to the Streamlit app's URL displayed in the terminal to interact with the application.

## Contributing

This project is in its initial stages and aims to grow with contributions. Feel free to fork the repository, make your changes, and submit a pull request.

## License

All Rights Reserved to Greg and Mina :)

## Project Structure

Counselor-Agent/
├── README.md
├── api/
│ ├── **init**.py
│ ├── chat_logic.py
│ └── main.py
├── client/
│ └── client.py
├── knowledgebase/
│ ├── ECS_faculty.json
│ ├── EECS_courses.json
│ └── departments.json
└── requirements.txt
