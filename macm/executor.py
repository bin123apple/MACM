from utils.gpt_robots import generate_from_excutor
from prompt.prompts import *

def Execute_steps(conditions, objectives, steps):
    '''
    Ask GPT to execute the steps and get final answer
    Input:
    conditions, objectives, steps (List, List, Str)
    Output:
    final answer (Str)
    '''
    messages = []
    numbered_conditions = "\n".join(f"{i + 1}. {condition}" for i, condition in enumerate(conditions))
    numbered_objective = "\n".join(f"{i + 1}. {objective}" for i, objective in enumerate(objectives))
    
    message = {
        "role": "user",
        "content": find_target.format(
            Objective=numbered_objective,
            Conditions=numbered_conditions,
            Steps=steps
        )
    }
    messages.append(message)
    
    message = {
        "role": "user",
        "content": box_target
    }
    messages.append(message)
    
    boxed_answer = generate_from_excutor(messages, max_tokens=512)
    return boxed_answer

def Find_Answer(conditions, objectives):
    '''
    ask GPT to find answer directly
    Input:
    conditions, objectives (List, List)
    Output:
    final answer (Str)
    '''
    messages = []
    numbered_conditions = "\n".join(f"{i + 1}. {condition}" for i, condition in enumerate(conditions))
    numbered_objective = "\n".join(f"{i + 1}. {objective}" for i, objective in enumerate(objectives))
    
    message = {
        "role": "user",
        "content": find_target.format(Objective=numbered_objective, Conditions=numbered_conditions)
    }
    messages.append(message)
    
    final_answer = generate_from_excutor(messages, max_tokens=512)
    return final_answer
