from utils.gpt_robots import generate_from_judge
from utils.gpt import Judge_if_got_Answer_from_GPT
from prompt.prompts import *

def Judge_condition(question,condition):
    '''
    ask GPT to Judge the thoughts from the thinker
    Input:
    Known_condtions, Condition from the thinker (List, Str)
    Output:
    True/False (Str)
    '''
    messages = []
    message = {
        "role": "user",
        "content": Judge_condtion.format(question = question,Initial_conditions = condition)
    }
    messages.append(message)
    T_or_F = generate_from_judge(messages, max_tokens = 4, model="gpt-4-1106-preview", temperature=0.7, n=1)
    return T_or_F


def Judge_statement(Known_condtions,condition_from_thinker):
    '''
    ask GPT to Judge the thoughts from the thinker
    Input:
    Known_condtions, Condition from the thinker (List, Str)
    Output:
    True/False (Str)
    '''
    messages = []
    numbered_conditions = "\n".join(f"{i + 1}. {condition}" for i, condition in enumerate(Known_condtions))
    message = {
        "role": "user",
        "content": Judge_T_F.format(Known_condtions = numbered_conditions,condition_from_thinker = condition_from_thinker)
    }
    messages.append(message)
    message = {
        "role": "user",
        "content": T_or_F_prompt
    }     
    messages.append(message)
    T_or_F = generate_from_judge(messages, max_tokens = 16, model="gpt-4-1106-preview", temperature=0.7, n=1)
    return T_or_F


def Judge_answer(Known_condtions,objectives):
    '''
    Ask GPT to Judge if we already got the answer
    Input:
    Known_condtions, objectives (List, List)
    Output:
    False / True ,answer (Str)
    '''
    messages = []
    numbered_conditions = "\n".join(f"{i + 1}. {condition}" for i, condition in enumerate(Known_condtions))
    numbered_Objective = "\n".join(f"{i + 1}. {objective}" for i, objective in enumerate(objectives))
    message = {
        "role": "user",
        "content": Judge_if_got_Answer.format(Known_condtions = numbered_conditions, 
                                              Objective = numbered_Objective)
    }
    messages.append(message)
    message = {
        "role": "user",
        "content": If_got_Answer_T_F
    }     
    messages.append(message)
    T_or_F = generate_from_judge(messages, 
                                 max_tokens = 4, 
                                 model="gpt-4-1106-preview", 
                                 temperature=0.7, n=1)
    return T_or_F

