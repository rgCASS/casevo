from abc import abstractmethod, ABCMeta


#LLM 接口基类
class LLM_INTERFACE(metaclass=ABCMeta):
    # 发送prompt
    @abstractmethod
    def send_message(self, prompt, json_flag=False):
        pass

    # 发送embedding
    @abstractmethod
    def send_embedding(self, text_list):
        pass
    
    # 获得langchain embedding的工具类
    @abstractmethod
    def get_lang_embedding(self):
        pass
