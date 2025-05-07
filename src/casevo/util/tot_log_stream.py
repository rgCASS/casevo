import json
import copy
import os


"""
TotLogStream类用于管理和处理日志流。
它收集和存储来自不同源的日志消息，以便于后续的处理和分析。
"""
class TotLogStream(object):
    # 存储model相关的日志
    model_log = []
    
    # 存储代理(agent)的日志
    agent_log = []
    
    # 代理(agent)的数量
    agent_num = 0
    
    # 存储额外的日志信息，以键值对的形式
    #extra_log = {}
    
    # 日志消息的偏移量，用于标记日志的位置
    offset = 0
    
    # 存储事件日志(总体日志)
    event_log = []
    
    # 标记是否有事件日志，False表示没有事件日志
    event_flag = False

    # 目标文件夹路径，用于存储或读取日志文件
    tar_folder = None
    
    # 缓冲区大小列表，用于管理日志流的缓冲
    buffer_size = 20

    current_num = 0
        
        
    @classmethod
    def init_log(cls, agent_num, tar_folder, if_event=False, buffer_size=20):
        """
        初始化日志类方法。
        
        该方法主要用于初始化不同类型的日志列表，以便在后续过程中记录模型和代理的行为。
        
        参数:
        - agent_num (int): 代理的数量，用于初始化相应数量的代理日志列表。
        - tar_folder (str): 目标文件夹的路径，用于存储日志文件。
        - if_event (bool): 是否启用事件日志的标志，默认为False。
        - buffer_size (int): 日志缓冲区的大小，用于控制写入日志文件的时机。
        
        返回:
        无返回值，但初始化了多个类变量用于记录各种日志。
        """
        # 初始化模型日志列表，用于记录模型相关的日志信息。
        cls.model_log = []
        
        # 初始化每个代理的日志列表，每个代理有一个独立的日志列表。
        cls.agent_log = [[] for i in range(agent_num)]
        
        # 保存代理的数量作为类变量，以便在后续过程中使用。
        cls.agent_num = agent_num
        
        # 初始化额外的日志字典，用于记录额外的信息。（已注释掉）
        # cls.extra_log = {}
        
        # 初始化偏移量变量，用于记录或调整日志中的某些数值。
        cls.offset = 0
        
        # 初始化事件日志列表，用于记录特定事件的日志信息。
        cls.event_log = []
        
        # 保存是否启用事件日志的标志。
        cls.event_flag = if_event
        
        # 保存目标文件夹路径，用于后续存储日志文件。
        cls.tar_folder = tar_folder
        
        cls.buffer_size = buffer_size
            

    @classmethod
    def set_offset(cls, tar_offset):
        """
        设置时间偏移量。

        参数:
        - tar_offset: 目标时间偏移量。
        """
        cls.offset = tar_offset

    @classmethod
    def add_model_log(cls, tar_ts, tar_type, tar_item):
        """
        添加模型日志条目。

        参数:
        - tar_ts: 时间戳。
        - tar_type: 日志类型。
        - tar_item: 日志项内容。
        """
        # 将日志条目添加到model_log列表中，包括时间戳、类型和内容。
        cls.model_log.append({
            'ts': tar_ts + cls.offset,
            'type': tar_type,
            'item': tar_item
        })
        # 如果事件标志为真，也将日志条目添加到event_log列表中。
        if cls.event_flag:
            cls.event_log.append({
                'ts': tar_ts + cls.offset,
                'owner': 'model',
                'type': tar_type,
                'item': tar_item
            })
        
        # 增加当前日志条目计数。
        cls.current_num += 1
        # 如果当前日志条目数达到缓冲区大小，触发写入日志操作。
        if cls.current_num >= cls.buffer_size:
            cls.write_log()

    @classmethod
    def add_agent_log(cls, tar_ts, tar_type, tar_item, tar_agent_id):
        """
        添加代理日志条目。
        
        参数:
        - tar_ts: 时间戳。
        - tar_type: 事件类型。
        - tar_item: 事件涉及的项目。
        - tar_agent_id: 代理ID。
        
        此方法首先在指定代理的日志中添加一个包含时间戳、类型和项目的条目。
        如果事件标志已设置，也会在事件日志中添加相应的条目。
        最后，检查当前日志条目数是否达到缓冲区大小，如果是，则写入日志。
        """
        cls.agent_log[tar_agent_id].append({
            'ts': tar_ts + cls.offset,
            'type': tar_type,
            'item': tar_item
        })
        if cls.event_flag:
            cls.event_log.append({
                'ts': tar_ts + cls.offset,
                'owner': 'agent_{}'.format(tar_agent_id),
                'type': tar_type,
                'item': tar_item
            })
        cls.current_num += 1
        if cls.current_num >= cls.buffer_size:
            cls.write_log()

    @classmethod
    def get_agent_log(cls, tar_agent_id):
        """
        获取指定代理的日志。
        
        参数:
        - tar_agent_id: 目标代理ID。
        
        返回:
        - 指定代理的日志列表。
        """
        return cls.agent_log[tar_agent_id]

    @classmethod
    def get_event_log(cls):
        """
        获取事件日志。
        
        返回:
        - 事件日志列表。
        """
        return cls.event_log

    @classmethod
    def write_log(cls):
        """
        将日志写入文件。
        
        此方法首先检查模型日志是否为空，如果不为空，则将其写入'model.txt'文件。
        然后，对于每个代理的日志，如果非空，则写入相应的'agent_{id}.txt'文件。
        如果事件标志已设置且事件日志非空，则将其写入'event.txt'文件。
        最后，对于任何额外日志，如果非空，则写入相应的文件。
        完成日志写入后，重置当前数量、模型日志、代理日志和事件日志。
        """
        if len(cls.model_log) > 0:
            res_str = ""
            for item in cls.model_log:
                res_str += json.dumps(item, ensure_ascii=False) + '\n'
            with open(os.path.join(cls.tar_folder, 'model.txt'), 'a') as f:
                f.write(res_str)
        
        for i in range(cls.agent_num):
            if len(cls.agent_log[i]) == 0:
                continue
            res_str = ""
            for item in cls.agent_log[i]:
                res_str += json.dumps(item, ensure_ascii=False) + '\n'
            with open(os.path.join(cls.tar_folder, 'agent_{}.txt'.format(i)), 'a') as f:
                f.write(res_str)
        
        if cls.event_flag and len(cls.event_log) > 0:
            res_str = ""
            for item in cls.event_log:
                res_str += json.dumps(item, ensure_ascii=False) + '\n'
            with open(os.path.join(cls.tar_folder, 'event.txt'), 'a') as f:
                f.write(res_str)
        '''
        for item in cls.extra_log:
            if len(cls.extra_log[item]) == 0:
                continue
            res_str = ""
            for item in cls.extra_log[item]:
                res_str += json.dumps(item, ensure_ascii=False) + '\n'
            with open(os.path.join(cls.tar_folder, '{}.txt'.format(item)), 'a') as f:
                f.write(res_str)
        '''
        cls.current_num = 0
        cls.model_log = []
        cls.agent_log = [[] for i in range(cls.agent_num)]
        cls.event_log = []
            


                


            