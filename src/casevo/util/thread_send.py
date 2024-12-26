import threading
import queue
import time

class ThreadSend:
    def __init__(self, thread_num=8):
        self.status = 'init' 
        self.task_list =  queue.Queue()
        self.threads_num = thread_num
        #self.task_num = 0
    def add_task(self, func, args):
        self.task_list.put([func, args])
        #self.task_num += 1
    
    def get_task_num(self):
        return self.task_list.qsize()

    def worker(self):
        while True:
            try:
                task = self.task_list.get(timeout=5)
                task[0](*task[1])
                self.task_list.task_done()
                time.sleep(5)
                if self.task_list.empty():
                    break
            except:
                break
    
    def start_thread(self):
        self.thread_list = []
        for i in range(self.threads_num):
            t = threading.Thread(target=self.worker)
            t.start()
            self.thread_list.append(t)
        self.task_list.join()