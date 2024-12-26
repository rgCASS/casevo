import os
from jinja2 import Environment, FileSystemLoader


#prompt
class Prompt:
    def __init__(self, tar_template, tar_factory):
        """
        初始化类实例。

        本构造函数旨在通过传入模板和工厂参数，为后续操作准备必要的属性。

        参数:
            tar_template: 用于生成目标文件的模板对象。模板对象应具备特定的结构和规则，以指导目标文件的创建。
            tar_factory: 工厂对象，用于根据模板生成目标文件。工厂对象应具备根据模板生成具体目标文件的方法和逻辑。

        返回:
            无返回值。本方法主要用于初始化类的实例属性。
        """
        self.template = tar_template
        self.factory = tar_factory
    
    def __get_prompt__(self, tar_dict):
        return self.template.render(**tar_dict)
    
    def send_prompt(self, ertra=None, agent=None, model=None):
        """
        发送提示信息。

        这个方法用于根据提供的参数生成并发送一个提示信息。它支持通过代理(agent)和模型(model)
        来定制提示信息的内容。额外参数(ertra)可以提供额外的信息来进一步定制提示。

        参数:
        - ertra: 额外参数，用于提供额外的定制信息，默认为None。
        - agent: 代理对象，如果提供，将使用代理的描述和上下文来定制提示信息。
        - model: 模型对象，如果提供，将使用模型的上下文来定制提示信息。

        返回:
        - 发送的提示信息的响应结果。
        """
        tar_agent = {}
        if agent:
            tar_agent = {
                "description": agent.description,
                "context": agent.context
            }
        tar_model = {}
        if model:
            tar_model = {
                "context": model.context
            }
             

        prompt_text = self.__get_prompt__({
            "agent": tar_agent,
            "model": tar_model,
            "extra": ertra})
        #print(prompt_text)
        #return ""
        return self.factory.__send_message__(prompt_text)

#prompt 工厂类
class PromptFactory:
    def __init__(self, tar_folder, llm):
        """
        初始化类的实例。

        该构造函数主要负责设置模板文件夹路径和语言模型，并验证模板文件夹的存在性。

        :param tar_folder: 模板文件夹的路径。必须是现有目录。
        :param llm: 语言模型的实例，用于处理自然语言。
        """
        self.prompt_folder = tar_folder
        if not os.path.exists(tar_folder):
            raise Exception("prompt folder not exist")
        self.env = Environment(loader=FileSystemLoader(tar_folder))
        self.llm = llm

    def get_template(self, tar_temp):
        """
        根据提供的模板名称，从特定文件夹中获取模板文件。
        
        此方法首先构造模板文件的完整路径，然后检查该文件是否存在。如果文件不存在，
        则抛出一个异常。如果文件存在，則使用环境变量加载该模板，并返回一个Prompt对象，
        该对象使用加载的模板和当前对象进行初始化。
        
        参数:
        tar_temp (str): 模板文件的名称。
        
        返回:
        Prompt: 使用加载的模板和当前对象初始化的Prompt对象。
        
        抛出:
        Exception: 如果指定的模板文件不存在，则抛出异常。
        """
        tar_file = os.path.join(self.prompt_folder, tar_temp)
        if not os.path.exists(tar_file):
            raise Exception("prompt file %s not exist" % tar_temp)
        res_temp = self.env.get_template(tar_temp)
        return Prompt(res_temp, self)

    def __send_message__(self, prompt_text):
        #print(prompt_text)
        return self.llm.send_message(prompt_text)
    

    
