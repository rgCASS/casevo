from casevo.base_component import BaseAgentComponent, BaseModelComponent
import re
import json
import threading
import queue
import time

#CoT步骤基类
class BaseStep:
    #对应的Prompt
    prompt = None
    #步骤id
    step_id = None
    def __init__(self, step_id, tar_prompt):
        self.prompt = tar_prompt
        self.step_id = step_id
    
    def pre_process(self, input, agent=None, model=None):
        """
        对输入数据进行预处理。

        本函数的目的是为了在进一步处理输入数据之前，对其进行必要的预处理。
        目前，函数实现了对输入的直接返回，但随着功能的扩展，可能会加入更多的预处理步骤。

        参数:
            input: 需要预处理的输入数据。
            agent: (可选) 代理对象，用于某些预处理任务。
            model: (可选) 模型对象，用于某些预处理任务。

        返回:
            经过预处理的输入数据。
        """
        return input

    def action(self, input, agent=None, model=None):
        """
        根据输入和上下文执行特定动作。

        本函数的核心职责是通过调用prompt模块的send_prompt方法，根据输入、代理和模型信息，
        发送一个提示并获取响应。这个方法通常用于在对话系统中生成回复。

        参数:
        input (str): 用户的输入，作为生成响应的依据。
        agent (Agent, optional): 代理对象，用于上下文相关信息的传递。默认为None。
        model (Model, optional): 模型对象，用于处理输入和生成响应。默认为None。

        返回:
        str: 生成的响应文本。
        """
        response = self.prompt.send_prompt(input, agent, model)
        return response
    
    def after_process(self, input, response, agent=None, model=None):
        """
        处理对话后的回调函数。
        
        该函数用于在对话处理完成后，收集并返回一些关键信息，如输入和最后一个响应。
        
        参数:
        - input: 用户的原始输入，用于记录或进一步处理。
        - response: 对于用户输入的机器人响应，用于分析或日志记录。
        - agent: 代理对象，通常用于访问对话管理相关功能。默认为None，表示不使用。
        - model: 模型对象，通常用于访问自然语言处理相关功能。默认为None，表示不使用。
        
        返回:
        - 一个字典，包含用户的原始输入和机器人的最后一个响应。
        """
        return {
            'input': input,
            'last_response': response
        }
    
    def get_id(self):
        return self.step_id

#用于选择题步骤
class ChoiceStep(BaseStep):
    """
    选择步骤类，用于处理需要用户进行选择的交互步骤。
    
    此类继承自一个基本的步骤类（假设名为Step），并添加了处理用户选择回答的逻辑。
    """
    def __init__(self, step_id, tar_prompt, choice_template=None):
        """
        初始化选择步骤。
        
        参数:
        step_id -- 步骤的唯一标识符。
        tar_prompt -- 需要用户回答的问题或提示。
        choice_template -- 用户选择的答案模板，用于定义有效答案的模式。
        
        如果没有提供choice_template，则默认为匹配大写字母的正则表达式。
        """
        super().__init__(step_id, tar_prompt)
        if choice_template:
            self.answer_template = choice_template
        else:
            self.answer_template = re.compile(r"[A-Z]")

    
    def after_process(self, input, response, agent=None, model=None):
        """
        处理对话后的后续操作。

        本函数用于分析响应中是否包含预期的答案模板匹配。如果没有匹配，则抛出异常；
        如果有匹配，则返回包含输入和匹配答案的字典。

        参数:
        input (str): 用户的输入语句。
        response (str): 机器人生成的响应语句。
        agent (Agent, optional): 代理对象，用于上下文操作。默认为None。
        model (Model, optional): 模型对象，用于预测和生成答案。默认为None。

        返回:
        dict: 包含输入和匹配到的答案的字典。

        抛出:
        Exception: 如果没有找到答案模板匹配，则抛出异常。
        """
        match = self.answer_template.search(response)
        if not match:
            raise Exception("No choice found")
        else:
            return {
                'input': input,
                'choice': match.group()
            }



class ScoreStep(BaseStep):
    """
    评分判断类，用于根据给定的步骤ID、目标提示和评分模板，判断和生成评分回答。
    """
    def __init__(self, step_id, tar_prompt, score_template=None):
        """
        初始化评分判断对象。
        
        如果提供了评分模板，则使用该模板作为答案模板；否则，使用默认的正则表达式作为答案模板，
        该正则表达式用于匹配整数或小数形式的评分。
        
        参数:
        - step_id: 步骤ID，表示这个评分判断属于哪个步骤。
        - tar_prompt: 目标提示，表示这个评分判断针对的是什么目标。
        - score_template: 评分模板，可选参数，用于定义评分的回答格式。
        """
        super().__init__(step_id, tar_prompt)
        if score_template:
            self.answer_template = score_template
        else:
            self.answer_template = re.compile(r"(-?\d+)(\.\d+)?")

    
    def after_process(self, input, response, agent=None, model=None):
        """
        处理对话代理的响应后，提取答案得分。

        此方法用于解析对话代理的响应，从中提取出答案的得分信息。

        :param input: 用户的输入语句。
        :param response: 对话代理的响应语句。
        :param agent: 对话代理实例，暂未使用。
        :param model: 语言模型实例，暂未使用。
        :return: 包含输入和得分的字典，如果找不到匹配则抛出异常。
        :raises Exception: 如果无法从响应中找到匹配的答案模板。
        """
        match = self.answer_template.search(response)
        if not match:
            raise Exception("No choice found")
        else:
            return {
                'input': input,
                'score': float(match.group())
            }

class JsonStep(BaseStep):
    """
    Json类
    """

    def __init__(self, step_id, tar_prompt, json_template=None):
        """
        初始化实例。

        :param step_id: 步骤ID，用于标识当前步骤。
        :param tar_prompt: 目标提示，用于说明这个步骤的目的或预期输出。
        :param json_template: JSON模板，用于生成答案的模板。如果未提供，则默认为一个匹配任意字符的正则表达式。
        """
        super().__init__(step_id, tar_prompt)
        if json_template:
            self.answer_template = json_template
        else:
            self.answer_template = re.compile(r"\{[\s\S]*\}")

    
    def after_process(self, input, response, agent=None, model=None):
        """
        处理对话代理的响应，提取并返回解析后的JSON数据。

        此方法用于解析对话代理返回的响应，确保其中包含预期的JSON数据。
        如果响应中没有找到JSON数据，则抛出异常。

        参数:
        input (str): 用户的输入。
        response (str): 对话代理的响应。
        agent (object): 对话代理对象，默认为None。
        model (object): 模型对象，默认为None。

        返回:
        dict: 包含用户输入和解析后的JSON数据的字典。

        抛出:
        Exception: 如果响应中没有找到JSON数据，则抛出此异常。
        """
        match = self.answer_template.search(response)
        if not match:
            raise Exception("No Json found")
        else:
            cur_json = json.loads(match.group())
            return {
                'input': input,
                'json': cur_json
            }

class ToolStep(BaseStep):
    def __init__(self, step_id, tar_prompt, callback=None):
        super().__init__(step_id, tar_prompt)
        self.callback = callback
    
    def pre_process(self, input, agent=None, model=None):
        input['arguments'] = None
        return input
    
    def action(self, input, agent=None, model=None):
        response = self.callback(input['arguments'])
        return response




#思维链
class ThoughtChain(BaseAgentComponent):
    #步骤
    steps = None
    #状态
    status = None
    #输入
    input_content = None
    #历史
    step_history = None
    #输出
    output_content = None 

    
    def __init__(self, agent, step_list):   
        """
        初始化链式操作对象。

        本构造函数用于创建一个表示链式操作的实例，它是由一系列步骤组成的。
        它继承自一个基础类，并通过传递特定参数来定制实例。

        :param agent: 代理对象，负责执行链中的步骤。
        :param step_list: 一个步骤列表，定义了链式操作的顺序和内容。
        """
        super().__init__(agent.component_id + "_chain", 'chain', agent)
        self.steps = step_list
        self.status = 'init'
    
    def set_input(self, input):
        """
        设置输入内容并更新状态。

        该方法用于在特定条件下更新对象的输入内容、步骤历史记录和状态。
        只有在状态为'init'或'finish'时才能调用此方法，调用后状态将变为'ready'。

        参数:
        input - 设置的输入内容。

        抛出:
        Exception - 如果当前状态不是'init'或'finish'，则抛出异常。

        """
        if self.status != 'init' and self.status != 'finish':
            raise Exception("set input error")
        else:
            self.input_content = input
            self.step_history = []
            self.status = 'ready'
        
    def run_step(self):
        """
        执行流程。
        
        此方法将根据当前状态执行流程中的单个步骤。它首先检查状态是否为就绪，然后逐个执行步骤，
        记录每个步骤的输入、输出和处理过程。执行完成后，更新状态为完成，并设置输出内容。
        
        抛出:
        Exception -- 如果当前状态不是就绪，则抛出异常。
        """
        if self.status != 'ready':
            raise Exception("running status error")
        
        self.status = 'running'
        last_input = self.input_content
        for item in self.steps:
            
            error_flag = True
            for i in range(3):
                try:
                    cur_input = item.pre_process(last_input, self.agent, self.agent.model)
                    
                    response = item.action(cur_input, self.agent, self.agent.model)
                    
                    cur_output = item.after_process(cur_input, response,  self.agent, self.agent.model)
                    error_flag = False
                    break
                except Exception as e:
                    print(e)
                    print("Thought Chain Retry..... %d"  % i)
            if error_flag:
                self.status = 'ready'
                raise Exception("Thought Chain Retry Failed")
                
            
            self.step_history.append({
                'id': item.get_id(),
                'input': cur_input,
                'output': cur_output
            })
            last_input = cur_output
        
        self.output_content = self.step_history[-1]['output']
        self.status = 'finish'
    
    def get_output(self):
        """
        获取输出内容。

        当对象状态为'finish'时，返回输出内容；否则，抛出异常。
        
        方法调用者可以通过此方法获取处理结果，必须在状态为'finish'时调用，否则将引发异常。

        Returns:
            self.output_content: 处理的输出内容。

        Raises:
            Exception: 如果状态不为'finish'，则抛出异常。
        """
        if self.status != 'finish':
            raise Exception("get output error")
        else:
            return self.output_content
    
    def get_history(self):
        """
        获取步骤历史记录。

        该方法用于在当前状态为'finish'时，返回步骤历史记录。如果状态不是'finish'，则抛出异常。

        返回:
            step_history: 步骤历史记录列表，包含所有的历史步骤。
        """
        if self.status != 'finish':
            raise Exception("get history error")
        else:
            return self.step_history
        

class ChainPool:
    def __init__(self, thread_num=8):
        self.status = 'init' 
        self.chain_list =  queue.Queue()
        self.threads_num = thread_num

    def add_chains(self, chains):
        for item in chains:
            self.chain_list.put(item)
        self.status = 'ready'

    def worker(self):
        while True:
            tar_chain = self.chain_list.get()
            tar_chain.run_step()
            self.chain_list.task_done()
            if self.chain_list.empty():
                break      
            time.sleep(5)
    
    def start_pool(self):
        if self.status != 'ready':
            raise Exception("start pool error")
        self.threads = []
        for _ in range(self.threads_num):
            t = threading.Thread(target=self.worker)
            t.start()
            self.threads.append(t)
        self.chain_list.join()
    
    
    

