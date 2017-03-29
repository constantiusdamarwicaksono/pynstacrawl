from queue import Queue
from threading import Thread

class Base_Crawler(Thread):
    __que = Queue();
    __exit_flag = False;

    def __init__(self):
        Thread.__init__(self);

    def get_queue(self):
        return self.__que;

    def get_exit_flag(self):
        return Base_Crawler.__exit_flag;

    def set_exit_flag(self,state):
        Base_Crawler.__exit_flag = state;
