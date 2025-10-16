import code
import os
from openai import OpenAI
import backoff 
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

def chat_gpt(prompt):
    response = client.chat.completions.create(
        model="DeepSeek-V3",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
        temperature=0.6,
        top_p=0.8,
        extra_body={"top_k": 20},
        frequency_penalty=1.1,
    )
    return response.choices[0].message.content.strip()

@backoff.on_exception(backoff.expo, Exception, max_tries=3)
def completions_with_backoff(**kwargs):
    return client.chat.completions.create(**kwargs)

def generate_from_GPT(prompts, max_tokens, model="DeepSeek-V3", temperature=0.6, n=3):
    """
    Generate answer from DeepSeek model with the given prompt.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=prompts,
            max_tokens=min(max_tokens, 1024),
            temperature=temperature,
            n=n,
            top_p=0.8,
            extra_body={"top_k": 20},
            frequency_penalty=1.1,
        )

        generated_ans = []
        for i, choice in enumerate(response.choices):
            generated_ans.append({
                "index": i,
                "message": {
                    "role": "assistant",
                    "content": choice.message.content
                },
                "finish_reason": getattr(choice, 'finish_reason', 'stop')
            })
        return generated_ans
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def Judge_if_got_Answer_from_GPT(prompts, max_tokens, model="DeepSeek-V3", temperature=0.6, n=1):
    """
    Generate answer from DeepSeek model with the given prompt.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=prompts,
            max_tokens=min(max_tokens, 1024),
            temperature=temperature,
            n=n,
            top_p=0.8,
            extra_body={"top_k": 20},
            frequency_penalty=1.1,
        )
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def Find_Answer_from_GPT(prompts, max_tokens, model="DeepSeek-V3", temperature=0.6, n=1):
    """
    Generate answer from DeepSeek model with the given prompt.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=prompts,
            max_tokens=min(max_tokens, 1024),
            temperature=temperature,
            n=n,
            top_p=0.8,
            extra_body={"top_k": 20},
            frequency_penalty=1.1,
        )
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
