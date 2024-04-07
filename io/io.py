import os
import re
import json
import random
from openai import OpenAI
os.environ["OPENAI_API_KEY"] = "" # Input your own API-Key
client = OpenAI()

def generate_Answer(prompts, model="gpt-4-1106-preview", temperature=0.7, n=1):
    message = prompts[0]["content"]
    assistant = client.beta.assistants.create(
        model=model,
        tools=[{"type": "code_interpreter"}],
    )

    thread = client.beta.threads.create()

    thread_message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message,
    )
    
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )  

    while run.status in ["queued", "in_progress"]:
        keep_retrieving_run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

        if keep_retrieving_run.status == "completed":
            print("\n")

            # Step 6: Retrieve the Messages added by the Assistant to the Thread
            all_messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )
            
            # Check the code part
            run_steps = client.beta.threads.runs.steps.list(
                thread_id=thread.id,
                run_id=run.id
            )
            # print("run_steps",run_steps)
            
            # Check other informations
            # print("------------------------------------------------------------ \n")
            # print(f"all messages:{all_messages}")
            # print(f"User: {thread_message.content[0].text.value}")
            # print(f"Assistant: {all_messages.data[0].content[0].text.value}")
            
            Assistant_response = all_messages.data[0].content[0].text.value
            return Assistant_response

        elif keep_retrieving_run.status == "queued" or keep_retrieving_run.status == "in_progress":
            pass
        else:
            print(f"Run status: {keep_retrieving_run.status}")
            break

def evaluate_dataset(folder_path, limit=50):
    for root, dirs, files in os.walk(folder_path):
        # Extract the subfolder name
        if root != folder_path:
            subfolder = os.path.relpath(root, folder_path)
            print(f"Processing subfolder: {subfolder}")
        else:
            print("Processing the main folder")

        # Find all JSON files in the current directory
        json_files = [f for f in files if f.endswith('.json')]

        # Randomly select up to 'limit' files
        selected_files = random.sample(json_files, min(limit, len(json_files)))

        for file in selected_files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r') as json_file:
                    data = json.load(json_file)
                    problem = data.get("problem")
                    if problem:
                        file_name = os.path.splitext(file)[0]  # Get the file name without extension
                        print(f"Working on {subfolder} problem: #{file_name}")
                        solution = data.get("solution")
                        if solution:
                            # Extract content within \\boxed{}
                            matched = re.search(r'(\\boxed\{.*\})', solution)
                            if matched:
                                print(f"Solution: {matched.group(1)}")
                            else:
                                print("Solution: No match found")
                        messages = []
                        message = {
                            "role": "user",
                            "content": problem
                        }
                        messages.append(message)
                        answer = generate_Answer(messages)
                        print(f'Answer:\n{answer}')
            except json.JSONDecodeError:
                print(f"Error reading file {file_path}")
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

# Call the function with the desired folder path
# evaluate_dataset('/path/to/your/folder')

                

if __name__ == "__main__":
    folder_path = "/MATH/test"
    evaluate_dataset(folder_path)