from queue import Queue
from threading import Thread

class BaseCrawler(Thread):
    __que = Queue();
    __exit_flag = False;

    def __init__(self):
        Thread.__init__(self);

    def get_queue(self):
        return self.__que;

    @classmethod
    def get_exit_flag(self):
        return BaseCrawler.__exit_flag;

    @classmethod
    def set_exit_flag(self,state):
        BaseCrawler.__exit_flag = state;
