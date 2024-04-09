import code
from openai import OpenAI
import backoff 


client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="",
) # Input your own API-Key

def chat_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


def generate_from_GPT(prompts, max_tokens, model="gpt-4-1106-preview", temperature=0.7, n=3):
    """
    Generate answer from GPT model with the given prompt.
    input:
        @max_tokens: the maximum number of tokens to generate; in this project, it is 8000 - len(fortran_code)
        @n: the number of samples to return
    return: a list of #n generated_ans when no error occurs, otherwise None

    return example (n=3):
        [
        {
        "index": 0,
        "message": {
            "role": "assistant",
            "content": "The meaning of life is subjective and can vary greatly"
        },
        "finish_reason": "length"
        },
        {
        "index": 1,
        "message": {
            "role": "assistant",
            "content": "As an AI, I don't have personal beliefs"
        },
        "finish_reason": "length"
        },
        {
        "index": 2,
        "message": {
            "role": "assistant",
            "content": "The meaning of life is subjective and can vary greatly"
        },
        "finish_reason": "length"
        }
    ]
    """
    import openai
    openai.api_key = "" # TODO

    try:
        result = completions_with_backoff(
            model = model, 
            messages = prompts, 
            temperature = temperature, 
            max_tokens = max_tokens, 
            n = n
        )

        generated_ans = result["choices"]
        return generated_ans
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def Judge_if_got_Answer_from_GPT(prompts, max_tokens, model="gpt-4-1106-preview", temperature=0.7, n=1):
    """
    Generate answer from GPT model with the given prompt.
    input:
        @max_tokens: the maximum number of tokens to generate; in this project, it is 8000 - len(fortran_code)
        @n: the number of samples to return
    return: a list of #n generated_ans when no error occurs, otherwise None

    return example (n=3):
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=prompts,
            max_tokens = max_tokens,
            temperature = temperature,
            n = n
        )
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
    
def Find_Answer_from_GPT(prompts, max_tokens, model="gpt-4-1106-preview", temperature=0.7, n=1):
    """
    Generate answer from GPT model with the given prompt.
    input:
        @max_tokens: the maximum number of tokens to generate; in this project, it is 8000 - len(fortran_code)
        @n: the number of samples to return
    return: a list of #n generated_ans when no error occurs, otherwise None

    return example (n=3):
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=prompts,
            max_tokens = max_tokens,
            temperature = temperature,
            n = n
        )
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None