from casevo.base_component import BaseAgentComponent, BaseModelComponent
import chromadb
from casevo.llm_interface import LLM_INTERFACE
from typing import List,Optional
import threading

#记忆元素
class MemoryItem:
    id = -1
    ts = -1
    source = ""
    target = ""
    #事件类型
    action = ""
    #内容
    content = ""
    
    #初始化
    def __init__(self, ts, source, target, action, content):
        self.ts = ts
        self.source = source
        self.target = target
        self.action = action
        self.content = content
    
    #将元素转换为字典类型
    def toDict(self):
        return { "ts": self.ts, "source": self.source, "target": self.target, "action": self.action, "content": self.content }
    

    @staticmethod
    def toList(memory_list, start_id):
        """
        将内存列表中的项目转换为包含内容、元数据和ID的列表形式。
        
        参数:
        memory_list: 存储项目对象的列表。
        start_id: 用于初始化项目ID的起始值。
        
        返回:
        content_list: 项目内容的列表。
        meta_list: 包含项目内容、ID等元数据的字典列表。
        id_list: 项目ID的字符串列表。
        """
        #内容列表
        content_list = []
        #元数据列表
        meta_list = []
        #id列表
        id_list = []
        for item in memory_list:
            cur_dict = item.toDict()
            cur_dict['id'] = start_id
            content_list.append(cur_dict["content"])
            meta_list.append(cur_dict)
            id_list.append(str(start_id))
            start_id += 1
        return content_list, meta_list, id_list

#Agent的Memory模块
class Memory(BaseAgentComponent):
    def __init__(self, component_id, agent, tar_factory):
        super().__init__(component_id, "memory", agent)
        #短记忆工厂
        self.short_memory_factory = tar_factory
        #本身的长记忆
        self.long_memory = None
        
        #最近一次reflection的短记忆ID
        self.last_id = -1

    def add_short_memory(self, source, target, action, content, ts=None):
        """
        向短期记忆中添加一条记忆项。

        这个方法用于在指定的时间戳下记录一条从source到target的action执行结果content。
        如果没有提供时间戳，则使用当前模拟时间。

        参数:
        source - 记忆项的来源。
        target - 记忆项的目标。
        action - 执行的动作。
        content - 动作的内容或结果。
        ts (可选) - 记忆项的时间戳。如果未提供，将使用当前模拟时间。

        返回:
        添加记忆项后的短期记忆状态。
        """
        # 如果没有提供时间戳，则使用当前模拟时间
        if not ts:
            ts = self.agent.model.schedule.time
        cur_memory = MemoryItem(ts, source, target, action, content)

        return self.short_memory_factory.__add_short_memory__([cur_memory])



    def search_short_memory_by_doc(self, content_list:List[str]):
        """
        根据文档内容列表在短时记忆中进行搜索。

        本方法通过调用短时记忆工厂的特定方法，来搜索与提供的文档内容列表相关的信息。
        这种搜索机制旨在快速定位和提取与当前处理的文档内容相关的历史信息，以支持更有效的决策或处理。

        参数:
        content_list (List[str]): 一个字符串列表，代表待搜索的文档内容。

        返回:
        search_result: 搜索结果，具体类型和结构取决于短时记忆工厂的实现。
        """
        return self.short_memory_factory.__search_short_memory_by_doc__(content_list, self.agent.component_id)
        
    def reflect_memory(self):
        """
        更新长期记忆并获取最新的记忆ID。

        本方法通过调用short_memory_factory的__reflect_memory__方法，来实现长期记忆的更新。
        这一过程涉及到当前代理(agent)的记忆同步，包括上一个记忆ID(last_id)和长期记忆(long_memory)的更新。

        返回:
            response: 更新后的长期记忆。
            last_id: 更新后的记忆ID，用于追踪和同步记忆状态。
        """
        response, last_id = self.short_memory_factory.__reflect_memory__(self.agent,self.last_id,self.long_memory)
        self.last_id = last_id
        self.long_memory = response
    def get_long_memory(self):
        #获得长期记忆
        return self.long_memory


#全局的Memory工厂
class MemeoryFactory(BaseModelComponent):
    def __init__(self, tar_llm : LLM_INTERFACE,  memory_num, prompt, model,tar_path=None):
        """
        初始化记忆模块。
        
        本模块旨在为特定的语言模型提供记忆功能，通过持久化存储来管理记忆条目。
        
        :param tar_llm: 目标语言模型接口，用于获取语言嵌入。
        :param tar_path: 向量数据库的路径。
        :param memory_num: 检索记忆条目的数量。
        :param prompt: 用于触发Reflection的提示。
        :param model: 关联的ABM模型。
        """
        
        #memory_log = MesaLog("memory")
        
        super().__init__("memory_factory", "memory_factory", model)
        
        self.llm = tar_llm
        if tar_path:
            self.client = chromadb.PersistentClient(path=tar_path)
        else:
            self.client = chromadb.Client()
        
        self.memory_collection = self.client.get_or_create_collection( "memory", embedding_function= self.llm.get_lang_embedding())
        self.memory_num = memory_num
        self.reflact_prompt = prompt

        self.lock = threading.Lock()
        #print(self.memory_collection.count())
    
    def create_memory(self, agent):
        """
        为一个agent建立Memory实体
        该方法为给定的代理创建一个特定于组件的记忆体。记忆体的名称由代理的组件ID和“_memory”后缀组成。
        这种记忆体机制有助于代理在执行任务时存储和检索信息。

        参数:
        - agent: 一个Agent实例，表示创建记忆体的代理。

        返回:
        - Memory: 一个Memory实例，用于存储和管理代理的记忆。
        """
        #cur_collection = self.client.get_or_create_collection(agent.component_id + "_memory", embedding_function= self.llm.get_lang_embedding())
        return Memory(agent.component_id + "_memory", agent, self)
    
    def __add_short_memory__(self, tar_memory:List[MemoryItem]) -> bool:
        """
        将目标记忆项添加到短期记忆中。

        这个方法封装了将记忆项添加到记忆集合的过程，包括计算开始位置、
        转换记忆项格式以及实际添加操作。

        :param tar_memory: 待添加的目标记忆项列表。
        :return: 添加操作是否成功的布尔值。
        """
        # 记录开始位置，用于后续计算新增记忆项的数量。
        self.lock.acquire()
        start_pos = self.memory_collection.count()
        # 将目标记忆项转换为统一的列表格式，准备添加到记忆集合中。
        content_list, meta_list, id_list = MemoryItem.toList(tar_memory, start_pos)
        # 实际添加记忆项到记忆集合中，并返回操作是否成功。
        res = self.memory_collection.add(documents=content_list, metadatas=meta_list, ids=id_list)
        self.lock.release() 
        return res
    
    def __search_short_memory_by_doc__(self, content_list:List[str], tar_agent):
        """
        根据文档内容和目标代理在记忆库中查询相关信息。
        
        这个方法用于在内部记忆集合中搜索与给定内容列表匹配且与目标代理相关的条目。
        它支持同时查询记忆的来源或目标为指定代理的记忆条目。
        
        参数:
        content_list (List[str]): 需要查询的记忆内容列表。
        tar_agent (str): 目标代理的标识，用于筛选记忆条目。
        
        返回:
        查询结果列表，包含与内容列表匹配且与目标代理相关的记忆条目。
        """
        # 根据内容列表和查询条件在记忆库中查询相关信息
        self.lock.acquire()
        res = self.memory_collection.query(
            query_texts=content_list,
            n_results=self.memory_num,
            where={"$or":[{"source": tar_agent},{"target": tar_agent}]}
        )
        self.lock.release()
        return res
    
    def __reflect_memory__(self, tar_agent, tar_pos, tar_long_opinion):
        """
        根据目标代理和位置进行reflection。

        该方法从内存集合中检索出指定代理之后的所有记忆项，并结合传入的长期意见，
        创建一个包含长期和短期记忆的字典。然后，它发送一个包含这些记忆的提示到反射prompt，
        以更新模型。最后，返回反射操作的结果以及最新的记忆项ID。

        参数:
        - tar_agent: 目标代理，记忆将基于此代理进行反射。
        - tar_pos: 目标位置，记忆点应在此位置之后。
        - tar_long_opinion: 目标长期意见，将被包含在反射的记忆中。

        返回:
        - response: 反射操作的结果。
        - last_id: 最新的记忆项ID。
        """
        self.lock.acquire()
        # 从内存集合中查询位于tar_pos之后且与tar_agent相关的记忆项
        memory_list = self.memory_collection.get(
            where={
                "$and":[
                    {"id":{"$gt":tar_pos}},
                    {"$or":[{"source": tar_agent.component_id},{"target": tar_agent.component_id}]}
                ]
            })
        self.lock.release()

        # 构建包含长期和短期记忆的字典
        tar_item = {
            'long_memory': tar_long_opinion,
            'short_memory': memory_list['metadatas']
        }
        
        # 发送包含记忆的提示，并获取反射操作的结果
        response = self.reflact_prompt.send_prompt(tar_item, tar_agent, self.model)
        
        # 初始化最后一个记忆项ID为-1，用于后续寻找最新的记忆项ID
        last_id = -1
        
        # 遍历记忆项ID列表，更新last_id为最大的ID值
        for item in memory_list['ids']:
            if int(item) > last_id:
                last_id = int(item)
        
        # 返回反射操作的结果和最新的记忆项ID
        return response, last_id

        

