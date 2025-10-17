import re
from utils.gpt_robots import generate_from_thinker
from prompt.prompts import *

def Analysis_conditions(question):
    '''
    ask GPT to determine the conditions and objectives of a question.
    Input:
    Original questions (Str)
    Output:
    conditions and objectives (List, List)
    '''
    messages = []
    message = {
        "role": "user",
        "content": Analysis_conditions_objective.format(Question=question)
    }
    messages.append(message)
    
    answer = generate_from_thinker(messages, max_tokens=256)
    
    if not answer or "Error" in answer:
        print(f"Error in generating analysis for question: {question}")
        return ["Error in analysis"], ["Error in analysis"]
    
    # 更健壮的解析逻辑
    try:
        # 检查是否包含 "Objective:" 分隔符
        if "Objective:" in answer:
            parts = answer.split("Objective:")
            conditions_text = parts[0].replace("Conditions:", "").strip()
            
            # 多种方式提取条件
            conditions = []
            if re.findall(r'\d\.\s*(.*)', conditions_text):
                conditions = re.findall(r'\d\.\s*(.*)', conditions_text)
            else:
                # 如果没有编号，按行分割
                conditions = [line.strip() for line in conditions_text.split('\n') if line.strip()]
            
            conditions = [condition.strip() for condition in conditions if condition.strip()]
            
            # 处理目标
            objectives_text = parts[1].strip() if len(parts) > 1 else ""
            objectives = []
            if re.search(r'\d\.\s+', objectives_text):
                objectives = re.findall(r'\d\.\s*(.*)', objectives_text)
            else:
                objectives = [obj.strip() for obj in objectives_text.split('\n') if obj.strip()]
            
            objectives = [objective.strip() for objective in objectives if objective.strip()]
            
            # 如果没有找到目标，使用默认目标
            if not objectives:
                objectives = ["Solve the problem"]
                
        else:
            # 如果没有标准格式，返回默认值
            print(f"Unexpected response format: {answer}")
            conditions = ["Analyze the problem conditions"]
            objectives = ["Solve the problem"]
            
        print(f"Parsed conditions: {conditions}")
        print(f"Parsed objectives: {objectives}")
        return conditions, objectives
        
    except Exception as e:
        print(f"Error parsing analysis response: {e}")
        print(f"Raw response: {answer}")
        return ["Error in parsing"], ["Error in parsing"]

def Fix_conditions(question, Initial_conditions):
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
        "content": Fix_conditions_prompt.format(question=question, Initial_conditions=Initial_conditions)
    }
    messages.append(message)
    
    fixed_condition = generate_from_thinker(messages, max_tokens=256)
    return fixed_condition

def Think_thoughts(conditions, objectives):
    '''
    Ask GPT to think about other conditions.
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
        "content": Discover_new_conditions.format(Known_conditions=numbered_conditions, Objective=numbered_objective)
    }
    messages.append(message)
    
    message = {
        "role": "user",
        "content": Summarize_Answer
    }
    messages.append(message)
    
    new_condition = generate_from_thinker(messages, max_tokens=256)
    
    if new_condition and "Error" not in new_condition:
        condition = [new_condition.strip()]
    else:
        new_condition = "I need to rethink it"
        condition = [new_condition.strip()]
    
    return condition

def Think_Steps(condition_from_thinker, objective_from_thinker):
    '''
    ask GPT to think about solution steps.
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
        "content": Determine_Steps.format(Known_conditions=numbered_conditions, Objective=numbered_objective)
    }
    messages.append(message)
    
    steps = generate_from_thinker(messages, max_tokens=256)
    return steps
