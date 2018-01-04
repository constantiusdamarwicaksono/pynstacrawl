import time, os, requests
from .BaseCrawler import BaseCrawler
from threading import Lock

class LinkProcessor(BaseCrawler):
    __name = 'Downloader ';
    __seq = 1;

    def __init__(self,_dir):
        super(LinkProcessor,self).__init__();
        self.name = self.__name + str(self.__seq);
        LinkProcessor.__seq += 1;
        self.dir = _dir;
        self.lock = Lock();

    def download_file(self,dir,name,link):
        if not os.path.isfile('./'+dir+'/'+name):
            print(self.name+' is processing '+str(link));
            try:
                r = requests.get(link);
                with open('./'+dir+'/'+name,'wb') as outfile:
                    outfile.write(r.content);
                outfile.close();
                return True
            except:
                return False
        else:
            print(name+' already exists');
            return False

    def run(self):
        while not self.get_exit_flag() :
            # if self.get_queue().empty() :
                # print(self.name+' is waiting for link ');
            item = self.get_queue().get();
            self.get_queue().task_done();
            if item is None:
                self.set_exit_flag(True);
                break;
            self.download_file(self.dir,item[item.rfind('/')+1:],item);
            # time.sleep(1);
        print(self.getName()+ ' terminated');
