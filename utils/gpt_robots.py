import os
from openai import OpenAI

os.environ["OPENAI_API_KEY"] = ""
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"], base_url="https://api.deepseek.com")

def generate_from_thinker(prompts, max_tokens, model="deepseek-chat", temperature=0.7, n=1):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=prompts,
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Thinker API Error: {e}")
        return "I need to rethink this problem."

def generate_from_judge(prompts, max_tokens, model="deepseek-chat", temperature=0.7, n=1):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=prompts,
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Judge API Error: {e}")
        return "False"

def generate_from_excutor(prompts, max_tokens, model="deepseek-chat", temperature=0.7, n=1):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=prompts,
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Executor API Error: {e}")
        return "Error in execution"
