from casevo.base_component import BaseAgentComponent, BaseModelComponent
import chromadb
from casevo.llm_interface import LLM_INTERFACE
from typing import List,Optional

class BackgroundItem:
    id = -1
    owner_id = ""
    
    bg_type = ""
    #内容
    content = ""
    extra = ""
    
    #初始化
    def __init__(self, owner_id, bg_type, content, extra = ""):
        self.owner_id = owner_id
        self.bg_type = bg_type
        self.content = content
        self.extra = extra
    
    #将元素转换为字典类型
    def toDict(self):
        return { "owner_id":self.owner_id, "bg_type":self.bg_type, "content": self.content, "extra": self.extra }
    

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


class Background(BaseAgentComponent):
    def __init__(self, component_id, agent, tar_factory):
        super().__init__(component_id, "background", agent)
        self.background_factory = tar_factory
    
    def add_backgrounds(self, content_list, bg_type_list = None, extra_list = None):
        add_list = []
        for i in range(len(content_list)):
            cur_type = 'default'
            if bg_type_list:
                cur_type = bg_type_list[i]
            
            cur_extra = ""
            if extra_list:
                cur_extra = extra_list[i]
            add_list.append(BackgroundItem(self.agent.component_id, cur_type, content_list[i], cur_extra))
        
        return self.background_factory.__add_short_memory__(add_list)

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
        return self.background_factory.__search_background__(content_list, self.agent.component_id)





#全局的Background工厂
class BackgroundFactory(BaseModelComponent):
    def __init__(self, tar_llm : LLM_INTERFACE,  background_num, model,tar_path=None):
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
        
        super().__init__("background_factory", "background_factory", model)
        
        self.llm = tar_llm
        if tar_path:
            self.client = chromadb.PersistentClient(path=tar_path)
        else:
            self.client = chromadb.Client()
        
        self.background_collection = self.client.get_or_create_collection("background", embedding_function= self.llm.get_lang_embedding())
        self.background_num = background_num
        #self.reflact_prompt = prompt

        
        #print(self.memory_collection.count())
    def is_empty(self):
        return self.background_collection.count() == 0


    def create_background(self, agent):
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
        return Background(agent.component_id + "_background", agent, self)
    
    def __add_backgrounds__(self, tar_memory:List[BackgroundItem]) -> bool:
        """
        将目标背景信息项添加到背景RAG中。

        :param tar_memory: 待添加的目标记忆项列表。
        :return: 添加操作是否成功的布尔值。
        """
        # 记录开始位置，用于后续计算新增记忆项的数量。
        self.lock.acquire()
        start_pos = self.background_collection.count()
        # 将目标记忆项转换为统一的列表格式，准备添加到记忆集合中。
        content_list, meta_list, id_list = BackgroundItem.toList(tar_memory, start_pos)
        # 实际添加记忆项到记忆集合中，并返回操作是否成功。
        res = self.background_collection.add(documents=content_list, metadatas=meta_list, ids=id_list)
        self.lock.release() 
        return res
    
    def __search_background__(self, content_list:List[str], tar_agent):
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
        res = self.background_collection.query(
            query_texts=content_list,
            n_results=self.background_num,
            where={"owner_id": tar_agent}
        )
        self.lock.release()
        return res.documents
    
    
