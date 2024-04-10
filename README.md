# Counselor Agent

## Project Overview

The Counselor Agent project is designed as an innovative tool to provide academic and counseling support to university students. Leveraging FastAPI and the OpenAI API, it integrates advanced AI-driven chat capabilities to assist users with a wide range of academic inquiries. This backend service is complemented by a Streamlit frontend, creating an interactive and user-friendly interface for working with an AI counselor.

## Environment Setup

1. **Install Anaconda or Miniconda**: Ensure you have Anaconda or Miniconda installed on your machine. If not, download and install from [Anaconda](https://www.anaconda.com/products/individual) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

2. **Create a Conda Environment**: Open your terminal and run the following command to create a new Conda environment named `counselor-agent` with Python 10.

   ```bash
   conda create --name counselor-agent python=10
   ```

3. **Activate the Environment**: Activate the newly created environment using:

   ```bash
   conda activate counselor-agent
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

1. **Start the FastAPI Server**: Inside the 'api' directory, launch the FastAPI server.

   ```bash
   uvicorn api.main:app --reload
   ```

2. **Launch the Streamlit Client**: In a new terminal window, ensure the `counselor-agent` environment is activated and run:

   ```bash
   streamlit run client.py
   ```

3. **Use the Application**: Navigate to the Streamlit app's URL displayed in the terminal to interact with the application.

## Knowledgebase Initialization

Before using the application, populate AstraDB with your knowledgebase data:

1. **Run the `knowledgebase_to_astradb.py` Script**:
   This script transfers your knowledgebase files to AstraDB, setting up the data for retrieval.
   ```bash
   python knowledgebase_to_astradb.py
   ```

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
├── knowledgebase_to_astradb.py
└── requirements.txt
