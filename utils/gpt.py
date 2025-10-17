from openai import OpenAI

client = OpenAI(
    api_key="",
    base_url="https://api.deepseek.com"
)

def chat_gpt(prompt):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def generate_from_GPT(prompts, max_tokens, model="deepseek-chat", temperature=0.7, n=3):
    """
    Generate answer from GPT model with the given prompt.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=prompts,
            max_tokens=max_tokens,
            temperature=temperature,
            n=n
        )
        return response.choices
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def Judge_if_got_Answer_from_GPT(prompts, max_tokens, model="deepseek-chat", temperature=0.7, n=1):
    """
    Generate answer from GPT model with the given prompt.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=prompts,
            max_tokens=max_tokens,
            temperature=temperature,
            n=n
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def Find_Answer_from_GPT(prompts, max_tokens, model="deepseek-chat", temperature=0.7, n=1):
    """
    Generate answer from GPT model with the given prompt.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=prompts,
            max_tokens=max_tokens,
            temperature=temperature,
            n=n
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
