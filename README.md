# Local Language Model Project with Ollama

This project demonstrates how to run two small-scale language models (Llama 3.2 and DeepSeek 1.5B) locally using Ollama. The program reads prompts from a text file, generates responses using the models, and displays the responses in the console.

## Prerequisites

Before running the project, ensure you have the following installed:

1. Download Ollama

2. Download Miniconda

3. Download VS Code

## Setup

1. Clone the Repository

2. Create a Conda Environment using the requirements.yaml file.
   conda env create -f requirements.yaml

3. Activate the Conda Environment using the command below.
   conda activate llm_project1

4. Install Ollama Models by using the command below in ollama terminal.
   ollama pull llama3.2
   ollama pull deepseek-r1:1.5b

## Running the Project

1. Prepare the Prompts File
   Create a file named `prompts.txt` in the project directory.
   Add your prompts to the file, one per line. 
   For example:
     A shocking Chinese AI advancement called DeepSeek is sending US stocks plunging.
     As sales slump, Kohl’s turns to a new CEO to bring back customers.
     Expect record-high egg prices for most of the year.

2. Run the Script
   Execute the Python script by using the command below.
   python run_llm.py

3. View the Output
   The responses from both models will be printed to the console.

