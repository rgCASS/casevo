
#import util.log

#所有组件的基类
class BaseComponent:
    #组件类型
    componet_type = ""
    #组件ID
    component_id = ""
    #日志模块
    #log = None
    #上下文
    context = None
    def __init__(self, component_id, coponent_type, tar_context):
        """
        初始化组件实例。

        该构造函数用于创建一个组件实例，并初始化其属性。

        参数:
        component_id (str): 组件的唯一标识符。
        coponent_type (str): 组件的类型，用于区分不同种类的组件。
        tar_context (object): 组件运行所需的上下文环境(用于prompt）。

        返回:
        None
        """
        
        self.component_id = component_id
        #self.log = log
        self.componet_type = coponent_type
        self.context = tar_context

    #def log_event(self, ts, tar_type, tar_event):
        """
        记录一个事件日志。

        该方法将给定的事件时间、类型和事件内容添加到日志记录中。
        这是一个重要的功能，用于跟踪和审计系统中的事件。

        参数:
            ts (int): 事件发生的时间戳。
            tar_type (str): 事件的目标类型，例如用户、设备等。
            tar_event (obj): 事件的具体内容或描述。
        """
        #self.log.add_log(ts, tar_type, tar_event)


#Agent组件的基类
class BaseAgentComponent(BaseComponent):
    #所属于的agent
    agent = None
    def __init__(self, component_id,  coponent_type, agent):
        super().__init__(component_id,  coponent_type, agent.context)
        self.agent = agent

#Model组件的基类
class BaseModelComponent(BaseComponent):
    model = None
    def __init__(self, component_id, coponent_type, model):
        super().__init__(component_id, coponent_type, model.context)
        self.model = model


