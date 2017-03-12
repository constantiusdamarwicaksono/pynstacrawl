#!/usr/bin/python3
import sys, signal, os
from lib.instagram_link_crawler import instagram_link_crawler
from lib.download_worker import download_worker
from lib.crawler_exception import *

def signal_handler(signal, frame):
        print("\nCrawling Stopped.\n");
        sys.exit(0);

def main():
    signal.signal(signal.SIGINT, signal_handler);
    if len(sys.argv) > 1:
        try :
            username = sys.argv[1];
            c = instagram_link_crawler(username);
            que = c.run();
            if not os.path.isdir('./'+username):
                os.mkdir('./'+username,0o775)
            download_worker.que = que;
            print('starting download');
            threads = [];
            for i in range(0,5):
                worker = download_worker('thread '+str(i+1),1,username);
                worker.start();
                threads.append(worker);
            for thread in threads:
                thread.join();
            print('all done stalker, everything stored in '+username+' folder');
        except Exception as e:
            print(e);
    else:
        print('please input username');

if __name__ == '__main__':
    main();
