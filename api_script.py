import json
import os
import requests

# Configuration Constants
# TODO: Replace with your actual OpenRouter API Key or set it as an environment variable

# Switched to Gemma 2 27B model slug on OpenRouter
MODEL_NAME = "google/gemma-2-27b-it"
INPUT_FILE_PATH = "text.txt"
OUTPUT_FILE_PATH = "responses.json"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

def read_prompts_from_file(file_path: str) -> list[str]:
    """Reads text input from a file line by line, stripping empty lines."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file '{file_path}' not found. Please create it first.")
    
    with open(file_path, "r", encoding="utf-8") as file:
        prompts = [line.strip() for line in file if line.strip()]
    return prompts

def query_openrouter_llm(prompt: str) -> str:
    """Sends a prompt to the OpenRouter API and returns the generated text response."""
    if OPENROUTER_API_KEY == "YOUR_OPENROUTER_API_KEY_HERE":
        return "Error: You forgot to replace 'YOUR_OPENROUTER_API_KEY_HERE' with your real OpenRouter API key!"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/devsoc-assignment",
        "X-Title": "DevSoc Assignment Script"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(
            OPENROUTER_API_URL, 
            headers=headers, 
            json=payload, 
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"\n[DEBUG] Status Code: {response.status_code}")
            print(f"[DEBUG] Response Body: {response.text}")
            
        response.raise_for_status()

        response_data = response.json()
        return response_data["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        return f"Error: Failed to fetch response from API. Details: {e}"

def save_responses_to_json(data: list[dict], output_path: str) -> None:
    """Saves structured response data into a JSON file."""
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
    print(f"\nSuccessfully saved responses to '{output_path}'.")

def main() -> None:
    """Main execution flow for processing text inputs through the LLM."""
    print(f"Reading inputs from {INPUT_FILE_PATH}...")
    try:
        prompts = read_prompts_from_file(INPUT_FILE_PATH)
    except FileNotFoundError as e:
        print(e)
        return

    if not prompts:
        print("The input file is empty. Add some text to process.")
        return

    results = []
    print(f"Processing {len(prompts)} prompt(s) using model: {MODEL_NAME}...\n")

    for index, prompt in enumerate(prompts, start=1):
        print(f"[{index}/{len(prompts)}] Sending prompt: '{prompt}'")
        llm_response = query_openrouter_llm(prompt)

        results.append({
            "prompt_id": index,
            "input_prompt": prompt,
            "model_used": MODEL_NAME,
            "llm_response": llm_response
        })

    save_responses_to_json(results, OUTPUT_FILE_PATH)
    print("Batch processing complete!")

if __name__ == "__main__":
    main()
