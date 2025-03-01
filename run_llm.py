# Import the Ollama library to interact with local language models
import ollama

# Function to generate responses using Ollama
def generate_response(model, prompt): 
    response = ollama.generate(model=model, prompt=prompt)  # To generate response
    # Limit the response to 100 words
    words = response['response'].split()  # Split the response into words
    if len(words) > 100:
        truncated_response = " ".join(words[:100])  # Join the first 100 words 
    else:
        truncated_response = response['response']  # Use the full response if it's <= 100 words
    
    return truncated_response  # Return the truncated response

# Function to read prompts from a text file
def read_prompts(file_path):
    try:
        with open(file_path, "r") as file:
            prompts = file.readlines() 
        print(f"Read {len(prompts)} prompts from {file_path}")
        return [prompt.strip() for prompt in prompts]
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")  # If prompts.txt file is not in same directory
        return []
    except Exception as e:
        print(f"An error occurred: {e}")  # If any error occurs
        return []

def main():
    models = {
        "llama3.2": "llama3.2",
        "deepseek-r1:1.5b": "deepseek-r1:1.5b"
    }

    # Read prompts from the prompts.txt
    prompts = read_prompts("prompts.txt")

    for model_name, model_id in models.items():
        print(f"\nGenerating responses using {model_name}...")  # To print model name
        for prompt in prompts:
            print(f"\nPrompt: {prompt}")  # To print the prompt which are in prompts.txt
            response = generate_response(model_id, prompt)  # To generate response
            print(f"Response: {response}")  # To print response

    print("\nAll responses generated and displayed successfully!")  # To say everything is completed

if __name__ == "__main__":
    main()  # Call the main function