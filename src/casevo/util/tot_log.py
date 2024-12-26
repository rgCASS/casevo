import json
import copy
import os

'''
__log_dict = {
    'model':[],
    'agent':[],
    'agent_num': 0,
    'extra':{},
    'offset': 0,
    'event':[],
    'event_flag':False
}
'''


class TotLog(object):
    model_log = []
    agent_log = []
    agent_num = 0
    extra_log = {}
    offset = 0
    event_log = []
    event_flag = False

    @classmethod
    def init_log(cls,agent_num, if_event=False):
        
        cls.model_log = []
        cls.agent_log = [[] for i in range(agent_num)]
        cls.agent_num = agent_num
        cls.extra_log = {}
        cls.offset = 0
        cls.event_log = []
        cls.event_flag = if_event
        

        '''
        __log_dict['model'] = []
        __log_dict['agent'] = [[] for i in range(agent_num)]
        __log_dict['agent_num'] = agent_num
        __log_dict['extra'] = {}
        __log_dict['offset'] = 0
        __log_dict['event_flag'] = if_event
        if if_event:
            __log_dict['event'] = []
        '''
    
    @classmethod
    def set_log(cls, tar_file, tar_offset, extra_list=[]):
        
        cls.offset = tar_offset
        with open(os.path.join(tar_file, 'model.json'), 'r') as f:
            cls.model_log = json.load(f)
        for i in range(cls.agent_num):
            with open(os.path.join(tar_file, 'agent_{}.json'.format(i)), 'r') as f:
                cls.agent_log[i] = json.load(f)
        if cls.event_flag:
            with open(os.path.join(tar_file, 'event.json'), 'r') as f:
                cls.event_log = json.load(f)
        for item in extra_list:
            with open(os.path.join(tar_file, '{}.json'.format(item)), 'r') as f:
                cls.extra_log[item] = json.load(f)

        
        '''
        __log_dict['offset'] = tar_offset
        with open(os.path.join(tar_file, 'model.json'), 'r') as f:
            __log_dict['model'] = json.load(f)
        for i in range(__log_dict['agent_num']):
            with open(os.path.join(tar_file, 'agent_{}.json'.format(i)), 'r') as f:
                __log_dict['agent'][i] = json.load(f)
        if __log_dict['event_flag']:
            with open(os.path.join(tar_file, 'event.json'), 'r') as f:
                __log_dict['event'] = json.load(f)
        for item in extra_list:
            with open(os.path.join(tar_file, '{}.json'.format(item)), 'r') as f:
                __log_dict['extra'][item] = json.load(f)
        '''

    @classmethod
    def add_model_log(cls, tar_ts, tar_type, tar_item):
        
        cls.model_log.append({
            'ts': tar_ts + cls.offset,
            'type': tar_type,
            'item': tar_item
        })
        if  cls.event_flag:
            cls.event_log.append({
                'ts': tar_ts + cls.offset,
                'owner': 'model',
                'type': tar_type,
                'item': tar_item
            })

        '''
        __log_dict['model'].append({
            'ts': tar_ts + __log_dict['offset'],
            'type': tar_type,
            'item': tar_item
        })
        if  __log_dict['event_flag']:
            __log_dict['event'].append({
                'ts': tar_ts + __log_dict['offset'],
                'owner': 'model',
                'type': tar_type,
                'item': tar_item
            })
        '''

    @classmethod
    def add_agent_log(cls, tar_ts, tar_type, tar_item, tar_agent_id):
        
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

        
        '''
        __log_dict['agent'][tar_agent_id].append({
            'ts': tar_ts,
            'type': tar_type,
            'item': tar_item
        })
        if  __log_dict['event_flag']:
            __log_dict['event'].append({
                'ts': tar_ts,
                'owner': 'agent_{}'.format(tar_agent_id),
                'type': tar_type,
                'item': tar_item
            })
        '''

    @classmethod
    def add_extra_log(cls, tar_ts, tar_type, tar_item, tar_name):
        
        cls.extra_log[tar_name].append({
            'ts': tar_ts + cls.offset,
            'type': tar_type,
            'item': tar_item
        })
        if cls.event_flag:
            cls.event_log.append({
                'ts': tar_ts + cls.offset,
                'owner': tar_name,
                'type': tar_type,
                'item': tar_item
            })

        
        '''
        __log_dict['extra'][tar_name].append({
            'ts': tar_ts,
            'type': tar_type,
            'item': tar_item
        })
        
        if __log_dict['event_flag']:
            __log_dict['event'].append({
                'ts': tar_ts,
                'owner': tar_name,
                'type': tar_type,
                'item': tar_item
            })
        '''

    @classmethod
    def get_agent_log(cls, tar_agent_id):
        return cls.agent_log[tar_agent_id]

    @classmethod
    def get_event_log(cls):
        return cls.event_log


    @classmethod
    def write_log(cls, tar_file):
        
        with open(os.path.join(tar_file, 'model.json'), 'w') as f:
            json.dump(cls.model_log, f, ensure_ascii=False)
        for i in range(cls.agent_num):
            with open(os.path.join(tar_file, 'agent_{}.json'.format(i)), 'w') as f:
                json.dump(cls.agent_log[i], f, ensure_ascii=False)
        if cls.event_flag:
            with open(os.path.join(tar_file, 'event.json'), 'w') as f:
                json.dump(cls.event_log, f, ensure_ascii=False)
        for item in cls.extra_log:
            with open(os.path.join(tar_file, '{}.json'.format(item)), 'w') as f:
                json.dump(cls.extra_log[item], f, ensure_ascii=False)
        
        '''
        with open(os.path.join(tar_file, 'model.json'), 'w') as f:
            json.dump(__log_dict['model'], f)
        
        for i in range(__log_dict['agent_num']):
            with open(os.path.join(tar_file, 'agent_{}.json'.format(i)), 'w') as f:
                json.dump(__log_dict['agent'][i], f)
        
        if __log_dict['event_flag']:
            with open(os.path.join(tar_file, 'event.json'), 'w') as f:
                json.dump(__log_dict['event'], f)
        
        for item in __log_dict['extra']:
            with open(os.path.join(tar_file, '{}.json'.format(item)), 'w') as f:
                json.dump(__log_dict['extra'][item], f)
        '''


            


        