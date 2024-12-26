import json
import copy
class MesaLog(object):
    def __init__(self, tar_name):
        self.log = []
        self.name = tar_name
        self.timeoffset = 0

    def add_log(self, tar_ts, tar_type, tar_item):
        cur_item = {
            'ts': tar_ts + self.timeoffset,
            'type': tar_type,
            'data': copy.deepcopy(tar_item)
        }
        self.log.append(cur_item)
    
    def set_log(self, tar_log, timeoffset):
        self.timeoffset = timeoffset
        self.log = tar_log
    
    def write_log(self, tar_file_name):
        with open(tar_file_name + '_%s.json' % self.name , 'w') as f:
            json.dump(self.log, f,ensure_ascii=False)
    
