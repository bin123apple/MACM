import re
from utils.gpt_robots import generate_from_thinker
from prompt.prompts import *

def Analysis_conditions(question):
    '''
    ask GPT to determine the conditions and objectives of a question.
    Input:
    Origianl questions (Str)
    Output:
    conditions and objectives (List, List)
    '''
    messages = []
    message = {
        "role": "user",
        "content": Analysis_conditions_objective.format(Question = question)
    }
    messages.append(message)
    # answer = generate_from_GPT(messages, max_tokens = 256, model="gpt-4-1106-preview", temperature=0.7, n=1)[0]["message"]["content"]
    answer = generate_from_thinker(messages, 
                                   max_tokens = 256, 
                                   model="gpt-4-1106-preview", 
                                   temperature=0.7,
                                   n=1)
    parts = answer.split("Objective:")
    conditions_text = parts[0].replace("Conditions:", "").strip()
    conditions = re.findall(r'\d\.\s*(.*)', conditions_text)
    conditions = [condition.strip() for condition in conditions]
    objectives_text = parts[1].strip()
    if re.search(r'\d\.\s+', objectives_text):
        # Extract objectives with numbers
        objectives = re.findall(r'\d\.\s*(.*)', objectives_text)
    else:
        # Split objectives by newline for unnumbered items
        objectives = objectives_text.split('\n')
    objectives = [objective.strip() for objective in objectives]
    return conditions,objectives


def Fix_conditions(question,Initial_conditions):
    '''
    ask GPT to fix the wrong initial condition of a question.
    Input:
    question and initial condition (Str, Str)
    Output:
    fixed condition (Str)
    '''
    messages = []
    message = {
        "role": "user",
        "content": Fix_conditions_prompt.format(question = question,Initial_conditions = Initial_conditions)
    }
    messages.append(message)
    # answer = generate_from_GPT(messages, max_tokens = 256, model="gpt-4-1106-preview", temperature=0.7, n=1)[0]["message"]["content"]
    fixed_condition = generate_from_thinker(messages, 
                                   max_tokens = 256, 
                                   model="gpt-4-1106-preview", 
                                   temperature=0.7, 
                                   n=1)
    return fixed_condition


def Think_thoughts(conditions,objectives):
    '''
    Ask GPT to think about other condtions.
    Input: 
    conditions and objective return from Analysis_conditions (List, List)
    Output:
    new conditions (List)
    '''
    messages = []
    numbered_conditions = "\n".join(f"{i + 1}. {condition}" for i, condition in enumerate(conditions))
    numbered_objective = "\n".join(f"{i + 1}. {objective}" for i, objective in enumerate(objectives))
    message = {
        "role": "user",
        "content": Discover_new_conditions.format(Known_conditions = numbered_conditions,Objective = numbered_objective)
    }
    messages.append(message)
    message = {
        "role": "user",
        "content": Summarize_Answer
    }
    messages.append(message)
    # new_condition = generate_from_GPT(messages, max_tokens = 128, model="gpt-4-1106-preview", temperature=0.7, n=1)[0]["message"]["content"]
    new_condition = generate_from_thinker(messages, 
                                          max_tokens = 128, 
                                          model="gpt-4-1106-preview", 
                                          temperature=0.7, 
                                          n=1)
    if new_condition:
        condition = [new_condition.strip()] # Single condition situation
        # pattern = r"Based on .+? we can get: .+? Reason: .+?\." # Multiple conditions situation
        # condition = re.findall(pattern, new_condition, re.DOTALL)

    else: # Avoid the run status fail situation
        new_condition = "I need to rethink it"
        condition = [new_condition.strip()]
    return condition


def Think_Steps(condition_from_thinker,objective_from_thinker):
    '''
    ask GPT to think about other condtions.
    Input: 
    conditions and objective return from Think_thoughts (List, List)
    Output:
    Steps for solving the problem (Str)
    '''
    messages = []
    numbered_conditions = "\n".join(f"{i + 1}. {condition}" for i, condition in enumerate(condition_from_thinker))
    numbered_objective = "\n".join(f"{i + 1}. {objective}" for i, objective in enumerate(objective_from_thinker))
    message = {
        "role": "user",
        "content": Determine_Steps.format(Known_conditions = numbered_conditions,Objective = numbered_objective)
    }
    messages.append(message)
    # steps = generate_from_GPT(messages, max_tokens = 256, model="gpt-4-1106-preview", temperature=0.7, n=1)[0]["message"]["content"]
    steps = generate_from_thinker(messages, 
                                  max_tokens = 256, 
                                  model="gpt-4-1106-preview", 
                                  temperature=0.7, 
                                  n=1)
    return steps
