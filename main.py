import os
import re
import json
import random
from prompt.prompts import *
from collections import Counter
from macm.executor import Execute_steps
from macm.judge import Judge_statement, Judge_answer, Judge_condition
from macm.thinker import Analysis_conditions, Think_thoughts, Think_Steps

def check_condition(question, condition, n):
    """
    Use several Judges to check the statement
    Input:
    conditions, unchecked_conditions, the number of the inspectors (List, Str, int)
    Output:
    True/False (bool)
    """
    for _ in range(n):
        result = Judge_condition(question, condition)
        if result and result.strip() == "False":
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
        if answer and ("False" in answer or "false" in answer):
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
    if if_got_answer and ("False" in if_got_answer or "false" in if_got_answer):
        return False
    return True

def check_if_got_answer(conditions, statement, n):
    for _ in range(n):
        if check_answer(conditions, statement) == False:
            return False
    return True    

def main(question, times, n, min_voters, max_voters):
    """
    Input question and get the final answer from multi-Agent system
    Input:
    question, the number of times new conditions are identified, the number of the inspectors (Str, int, int)
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
            
            # 增强错误处理
            try:
                conditions, objectives = Analysis_conditions(question)
                if "Error" in conditions or "Error" in objectives:
                    print(f"Error in analysis for voter {voter_count}, skipping...")
                    continue
                    
                print(f"Conditions found: {len(conditions)}")
                print(f"Objectives found: {len(objectives)}")
                
            except Exception as e:
                print(f"Error in Analysis_conditions: {e}")
                continue
                
            Initial_condition_numbers = len(conditions)
            
            # Think thoughts
            for time in range(times):
                print(f"\n# {voter_count} Thinker is thinking new thoughts (round {time + 1})...")
                try:
                    unchecked_conditions = Think_thoughts(conditions, objectives)
                    checked_conditions = []
                    
                    for unchecked_condition in unchecked_conditions:
                        print(f"\n# {voter_count} Judge is checking conditions...")
                        if check_statement(conditions, unchecked_condition, n):
                            # 提取条件内容
                            start = unchecked_condition.find("we can get: ")
                            if start != -1:
                                unchecked_condition = unchecked_condition[start + len("we can get: "):]
                                unchecked_condition = unchecked_condition.split("Reason:")[0].strip()
                            checked_conditions.append(unchecked_condition)
                            print(f"New condition added: {unchecked_condition}")
                    
                    conditions.extend(checked_conditions)
                    
                    # 检查是否已经得到答案
                    if_got_answer = check_if_got_answer(conditions, objectives, 1)
                    if if_got_answer:
                        print("Answer found in conditions, breaking early.")
                        break
                        
                except Exception as e:
                    print(f"Error in Think_thoughts round {time + 1}: {e}")
                    continue
            
            print(f"\n# {voter_count} thinker is thinking steps...")
            try:
                steps = Think_Steps(conditions, objectives)
                print(f"Steps generated: {steps[:100]}...")  # 只打印前100个字符
            except Exception as e:
                print(f"Error in Think_Steps: {e}")
                steps = "Error generating steps"
            
            print(f"\n# {voter_count} Executor is trying to calculate the answer...")
            try:
                final_answer = Execute_steps(conditions, objectives, steps)
                print(f"Executor response: {final_answer}")
            except Exception as e:
                print(f"Error in Execute_steps: {e}")
                final_answer = "Error in execution"
            
            # 提取答案
            Answer_boxed = "No answer found"
            if final_answer and "Error" not in final_answer:
                Answer_match = re.search(r'\\boxed\{(.*?)\}', final_answer)
                if Answer_match:
                    Answer_boxed = Answer_match.group(1)
                else:
                    # 如果没有找到boxed格式，尝试其他格式
                    Answer_boxed = final_answer.strip()[:100]  # 限制长度
            
            possible_answers.append(Answer_boxed)
            print(f"Voter {voter_count} answer: {Answer_boxed}")
            
            # 检查投票状态
            if voter_count >= min_voters:
                counter = Counter(possible_answers)
                most_common = counter.most_common(1)
                if most_common:
                    most_votes = most_common[0][1]
                    tie_count = len([count for count in counter.values() if count == most_votes])
                    tie = tie_count > 1
                    
                    if tie:
                        print(f"\nTie detected. Current votes: {dict(counter)}")
                    else:
                        print(f"\nClear winner found. Current votes: {dict(counter)}")
                
                if voter_count >= max_voters:
                    print("\nReached maximum voter limit.")
                    break
        
        # 确定最终答案
        if possible_answers:
            counter = Counter(possible_answers)
            most_possible_answer, count = counter.most_common(1)[0]
            print(f"\nFinal answer after {voter_count} voters: {most_possible_answer} (votes: {count})")
            return most_possible_answer
        else:
            print("\nNo answers generated.")
            return "No answer generated"
            
    except Exception as e:
        print(f"Error in main processing: {e}")
        return f"Error: {e}"

def evaluate_dataset(folder_path, times, n, limit=5):
    all_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                all_files.append(file_path)

    random.shuffle(all_files)

    for count, file_path in enumerate(all_files[:limit]):
        with open(file_path, 'r') as json_file:
            try:
                data = json.load(json_file)
                problem = data.get("problem")
                if problem:
                    print(f"\n{'='*50}")
                    print(f"#{count} Problem:\n", problem)
                    solution = data.get("solution")
                    if solution:
                        matched = re.search(r'(\\boxed\{.*\})', solution)
                        if matched:
                            print(f"#{count} Solution: {matched.group(1)}")
                        else:
                            print(f"#{count} Solution: No boxed answer found")
                    
                    # 调用主函数处理问题
                    main(problem, times, n, min_voters=3, max_voters=5)
                    print(f"{'='*50}\n")
                    
            except json.JSONDecodeError:
                print(f"Error reading file {file_path}")
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")
                              
if __name__ == "__main__":
    n = 1  # verification times
    times = 3  # 减少挖掘次数以加快测试
    min_voters = 2  # 最小投票人数
    max_voters = 3  # 最大投票人数
    
    # 测试一个简单问题
    test_question = "Louis earns a base monthly salary of $1200 with 5% commission on sales. For a month with $25000 in sales, what are Louis's total earnings?"
    
    print("Starting MACM system with test question...")
    result = main(test_question, times, n, min_voters, max_voters)
    print(f"\nFinal Result: {result}")
