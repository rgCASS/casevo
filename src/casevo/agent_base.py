from abc import abstractmethod

import mesa
from casevo.chain import ThoughtChain

#用于构建Agent的基类
class AgentBase(mesa.Agent):
    def __init__(self, unique_id, model, description, context):
        """
        初始化代理类实例。

        :param unique_id: 代理的唯一标识符。
        :param model: 代理所处的model环境。
        :param description: 代理对应的人设描述信息。
        :param context: agent的上下文（用于Prompt）。
        """
        # 调用父类的初始化方法，传递unique_id和model
        super().__init__(unique_id, model)
        
        # 生成并分配一个特定于agent的组件ID
        self.component_id = "agent_" + str(unique_id)
        
        # 初始化一个日志对象，用于记录代理的操作日志
        #self.log = MesaLog(self.component_id)
        
        # 设置代理的描述信息
        self.description = description
        
        # 设置代理的操作上下文
        self.context = context
        
        # 根据模型的内存工厂创建一个内存对象，用于存储代理的状态信息
        self.memory = model.memory_factory.create_memory(self)
    def setup_chain(self, chain_dict):
        """
        初始化思考链集合。

        通过遍历给定的思考链字典，为每个思考链创建一个ThoughtChain实例，并存储在self.chains中。
        这允许后续操作和访问这些思考链。

        参数:
        chain_dict (dict): 一个键值对字典，其中键代表思考链的标识符，值是对应的思考链数据。

        返回:
        无
        """
        # 初始化一个空的思考链字典
        self.chains = {}
        # 遍历传入的思考链字典
        for key, cur_chain in chain_dict.items():
            # 创建一个ThoughtChain实例，传入当前对象和当前的思考链数据
            tmp_thought = ThoughtChain(self, cur_chain)
            # 将创建的ThoughtChain实例存储在self.chains中，以键为标识符
            self.chains[key] = tmp_thought

    @abstractmethod
    def step(self):
        # 定义抽象方法，用于代理的每一步操作
        pass

    