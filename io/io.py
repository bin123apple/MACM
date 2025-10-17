import os
import re
import json
import random
from openai import OpenAI

os.environ["OPENAI_API_KEY"] = ""
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"], base_url="https://api.deepseek.com")

def generate_Answer(prompts, model="deepseek-chat", temperature=0.7, n=1):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=prompts,
            temperature=temperature,
            max_tokens=512
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating answer: {e}")
        return None

def evaluate_dataset(folder_path, limit=50):
    for root, dirs, files in os.walk(folder_path):
        if root != folder_path:
            subfolder = os.path.relpath(root, folder_path)
            print(f"Processing subfolder: {subfolder}")
        else:
            print("Processing the main folder")

        json_files = [f for f in files if f.endswith('.json')]
        selected_files = random.sample(json_files, min(limit, len(json_files)))

        for file in selected_files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r') as json_file:
                    data = json.load(json_file)
                    problem = data.get("problem")
                    if problem:
                        file_name = os.path.splitext(file)[0]
                        print(f"Working on {subfolder} problem: #{file_name}")
                        solution = data.get("solution")
                        if solution:
                            matched = re.search(r'(\\boxed\{.*\})', solution)
                            if matched:
                                print(f"Solution: {matched.group(1)}")
                            else:
                                print("Solution: No match found")
                        
                        messages = [{"role": "user", "content": problem}]
                        answer = generate_Answer(messages)
                        print(f'Answer:\n{answer}')
            except json.JSONDecodeError:
                print(f"Error reading file {file_path}")
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

if __name__ == "__main__":
    folder_path = "/MATH/test"
    evaluate_dataset(folder_path)
