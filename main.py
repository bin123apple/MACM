# -*- coding: utf-8 -*-
import sys
import io
import os
import re
import json
import random
from prompt.prompts import *
from collections import Counter
from macm.executor import Execute_steps
from macm.judge import Judge_statement, Judge_answer, Judge_condition
from macm.thinker import Analysis_conditions, Think_thoughts, Think_Steps
from dotenv import load_dotenv

# 设置UTF-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 加载 .env 文件
load_dotenv()

def check_condition(question, condition, n):
    """
    Use several Judges to check the statement
    Input:
    conditions, unchecked_conditions, the number of the inspectors (List, Str, int)
    Output:
    True/False (bool)
    """
    for _ in range(n):
        if Judge_condition(question, condition).strip() == "False":
            return False
    return True

def check_statement(conditions, statement, n):
    """
    Use several Judges to check the statement
    Input:
    conditions, unchecked_conditions, the number of the inspectors (List, Str, int)
    Output:
    True/False (bool)
    """
    for _ in range(n):
        answer = Judge_statement(conditions, statement)
        if "False" in answer or "false" in answer:
            return False
    return True

def check_answer(conditions, statement):
    """
    Use several Judges to check the answer
    Input:
    unchecked_conditions, the number of the inspectors (Str, int)
    Output:
    True/False (bool)
    """
    if_got_answer = Judge_answer(conditions, statement)
    if "False" in if_got_answer or "false" in if_got_answer:
        return False
    return True

def check_if_got_answer(conditions, statement, n):
    for _ in range(n):
        if check_answer(conditions, statement) == False:
            return False
    return True    

def main(question, times, n, min_voters, max_voters):
    """
    Input question and get the final answer from muti-Agent got
    Input:
    quesion, the number of times new conditions are identified, the number of the inspectors  (Str, int, int)
    Output:
    final answer (Str)
    """
    possible_answers = []
    try:
        voter_count = 0
        tie = True
        
        # Vote
        while tie or voter_count < min_voters:
            voter_count += 1
            print(f"\n# {voter_count} Thinker is analyzing the question...")
            
            try:
                conditions, objectives = Analysis_conditions(question)
                print(f"分析得到的条件: {conditions}")
                print(f"分析得到的目标: {objectives}")
            except Exception as e:
                print(f"分析条件时出错: {e}")
                conditions, objectives = [f"问题: {question}"], [f"解决问题: {question}"]
            
            Initial_condition_numbers = len(conditions)
            
            # Think thoughts
            for time in range(times):
                print(f"\n# {voter_count} Thinker is thinking new thoughts...")
                unchecked_conditions = Think_thoughts(conditions, objectives)
                checked_conditions = []
                for unchecked_condition in unchecked_conditions:
                    print(f"\n# {voter_count} Judge is checking conditions...")
                    if check_statement(conditions, unchecked_condition, n):
                        start = unchecked_condition.find("we can get: ")
                        if start != -1:
                            unchecked_condition = unchecked_condition[start + len("we can get: "):]
                            unchecked_condition = unchecked_condition.split("Reason:")[0]
                        checked_conditions.append(unchecked_condition)
                conditions = conditions + checked_conditions
                if_got_answer = check_if_got_answer(conditions, objectives, 1)
                if if_got_answer:
                    break
            
            print(f"\n# {voter_count} thinker is thinking steps...")
            steps = Think_Steps(conditions, objectives)
            
            print(f"\n# {voter_count} Executor is trying to calculate the answer...")
            final_answer = Execute_steps(conditions, objectives, steps)
            print(f"Executor 返回的答案: {final_answer}")
            
            # 改进答案提取逻辑
            Answer_boxed = extract_final_answer(final_answer)
            print(f"提取的最终答案: {Answer_boxed}")
            
            possible_answers.append(Answer_boxed)
            
            if voter_count >= min_voters:
                counter = Counter(possible_answers)
                most_votes = counter.most_common(1)[0][1]  
                tie_count = len(list(filter(lambda x: x[1] == most_votes, counter.items())))
                
                tie = tie_count > 1
                if tie:
                    print("\n存在平局，需要增加投票者。")
                if voter_count >= max_voters:
                    print("\n达到最大投票者限制。")
                    break
        
        if possible_answers:
            counter = Counter(possible_answers)
            most_possible_answer, count = counter.most_common(1)[0]
            print(f"\n最终答案是: {most_possible_answer}")
            return most_possible_answer
        else:
            print("\n没有生成任何答案。")
            return "没有答案"
            
    except Exception as e:
        print(f"处理文件时出错: {e}")
        return f"错误: {e}"

def extract_final_answer(final_answer):
    """
    从执行器的响应中提取最终答案
    """
    if not final_answer:
        return "无答案"
    
    # 方法1: 尝试提取 \\boxed{} 格式
    Answer = re.search(r'\\boxed\{(.*?)\}', final_answer)
    if Answer:
        return Answer.group(1).strip()
    
    # 方法2: 尝试提取 ``` 代码块格式
    Answer = re.search(r'```(?:.*?)\n(.*?)\n```', final_answer, re.DOTALL)
    if Answer:
        return Answer.group(1).strip()
    
    # 方法3: 尝试提取引号内的内容
    Answer = re.search(r'["\'](.*?)["\']', final_answer)
    if Answer:
        return Answer.group(1).strip()
    
    # 方法4: 如果以上都不行，返回前100个字符
    if len(final_answer) > 100:
        return final_answer[:100] + "..."
    else:
        return final_answer.strip()
    
if __name__ == "__main__":
    n = 1  # verification times
    times = 5  # The upper limit of the mining times
    min_voters = 3  # min number of voters (降低以便测试)
    max_voters = 5  # max number of voters (降低以便测试)
    question = "用中文回答我什么是费马大定理"  # Input your own question

    main(question, times, n, min_voters, max_voters)
