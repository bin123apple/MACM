import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 模力方舟 DeepSeek 配置
API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise RuntimeError("The environment variable API_TOKEN is not set correctly. Please check your .env file.")

client = OpenAI(
    base_url="https://ai.gitee.com/v1",
    api_key=API_TOKEN,
    default_headers={"X-Failover-Enabled": "true"},
)

def generate_from_thinker(prompts, max_tokens, model="DeepSeek-V3", temperature=0.6, n=1):
    """
    Thinker role using DeepSeek model
    """
    try:
        system_message = {
            "role": "system",
            "content": "You are a thinker. I need you to help me think about some problems. You need to provide me the answer based on the format of the example."
        }
        
        all_messages = [system_message] + prompts
        
        response = client.chat.completions.create(
            model=model,
            messages=all_messages,
            max_tokens=min(max_tokens, 1024),
            temperature=temperature,
            n=n,
            top_p=0.8,
            extra_body={"top_k": 20},
            frequency_penalty=1.1,
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"An error occurred in generate_from_thinker: {e}")
        return "I need to rethink this problem."

def generate_from_judge(prompts, max_tokens, model="DeepSeek-V3", temperature=0.6, n=1):
    """
    Judge role using DeepSeek model
    """
    try:
        system_message = {
            "role": "system", 
            "content": "You're a judge. I need you to make judgments on some statements. Please provide clear and fair judgments."
        }
        
        all_messages = [system_message] + prompts
        
        response = client.chat.completions.create(
            model=model,
            messages=all_messages,
            max_tokens=min(max_tokens, 1024),
            temperature=temperature,
            n=n,
            top_p=0.8,
            extra_body={"top_k": 20},
            frequency_penalty=1.1,
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"An error occurred in generate_from_judge: {e}")
        return "False"

def generate_from_excutor(prompts, max_tokens, model="DeepSeek-V3", temperature=0.6, n=1):
    """
    Executor role using DeepSeek model
    """
    try:
        system_message = {
            "role": "system",
            "content": "You're an executor. I need you to calculate the final result based on some conditions and steps. You need to provide me the answer based on the format of the examples."
        }
        
        all_messages = [system_message] + prompts
        
        response = client.chat.completions.create(
            model=model,
            messages=all_messages,
            max_tokens=min(max_tokens, 1024),
            temperature=temperature,
            n=n,
            top_p=0.8,
            extra_body={"top_k": 20},
            frequency_penalty=1.1,
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"An error occurred in generate_from_excutor: {e}")
        return "False"
