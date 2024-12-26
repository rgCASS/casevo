import mesa
from casevo.memory import MemeoryFactory
from casevo.prompt import PromptFactory
from casevo.util.thread_send import ThreadSend

class OrederTypeActivation(mesa.time.RandomActivationByType):
    def add_timestemp(self):
        self.time += 1
        self.steps += 1

#模型定义基类
class ModelBase(mesa.Model):
    def __init__(self, tar_graph, llm, context=None, prompt_path='./prompt/', memory_path=None, memory_num=10, reflect_file='reflect.txt', type_schedule=False):
        super().__init__()
        #设置网络
        self.grid = mesa.space.NetworkGrid(tar_graph)
    
        #Agent调度器
        if type_schedule:
            self.schedule = OrederTypeActivation(self)
        else:
            self.schedule = mesa.time.RandomActivation(self)

        #设置日志
        #self.log = MesaLog("model")
        
        #self.event_log = None
        #设置Event日志
        #if event_log:
        #    self.event_log = MesaLog("event")
        
        #上下文信息
        self.context = context
        
        #设置基座模型
        self.llm = llm

        #设置prompt工厂
        self.prompt_factory = PromptFactory(prompt_path, self.llm)
        
        #反思prompt
        reflect_prompt = self.prompt_factory.get_template(reflect_file)


        #设置memory工厂
        self.memory_factory = MemeoryFactory(self.llm, memory_num, reflect_prompt, self, memory_path)

        #初始化agent列表
        self.agent_list = []
    
    def add_agent(self, tar_agent, node_id):
        """
        将一个新的代理添加到系统中。

        此方法将代理添加到代理列表中，将其加入调度器，并将其放置在指定的节点上。

        参数:
        - tar_agent: 要添加的代理对象。
        - node_id: 代理将被放置的节点ID。
        """
        # 将新代理添加到代理列表中
        self.agent_list.append(tar_agent)
        # 将代理添加到调度器中，以便它可以被调度和执行任务
        self.schedule.add(tar_agent)
        # 在网格中的指定节点上放置代理
        self.grid.place_agent(tar_agent, node_id)
    
    #def reflect(self):
        """
        让所有代理对象进行反思操作。
        
        此方法遍历代理列表，并调用每个代理对象的reflect方法，让它们进行自我反思。
        """
        
        #cur_thread = ThreadSend()
        #for cur_agent in self.agent_list:
            #cur_thread.add_task(cur_agent.reflect, ())
        
        #cur_thread.start_thread()


    
    def step(self):
        """
        执行模拟步骤。
        
        此方法推进模拟时间的一个步骤，并管理所有调度对象的更新。它不接受任何参数，也不返回任何有意义的值，
        主要是为了触发模拟过程的推进。
        
        Returns:
            int: 始终返回0，作为步骤执行的结果指示。
        """
        self.schedule.step()
        return 0
    '''
    def write_log(self, tar_file_name):
        #输出log
        self.log.write_log(tar_file_name)
        for cur_agent in self.agent_list:
            cur_agent.log.write_log(tar_file_name)  
    ''' 




        
