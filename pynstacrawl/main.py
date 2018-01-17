"""
created by damar
"""
import sys, signal, requests, argparse
from lib.link_producer import LinkProducer
from lib.link_processor import LinkProcessor
from lib.base_crawler import BaseCrawler

def signal_handler(signal, frame):
    print("\nAttempting to stop crawling process!!\n");
    BaseCrawler.set_exit_flag(True);
    sys.exit(0);

def init_parser():
    parser = argparse.ArgumentParser();
    parser.add_argument('username',help='instagram account username');
    parser.add_argument('-c','--use_cookies',help="use firefox cookies",action="store_true");
    args = parser.parse_args()
    return args;

def show_banner():
    banner=\
"""
_____________________________________________________________
 _                                               _
| | ___ _ __ ___  _ __ ___   ___  __ _ _ __ __ _| |__  _   _
| |/ _ \ '_ ` _ \| '_ ` _ \ / _ \/ _` | '__/ _` | '_ \| | | |
| |  __/ | | | | | | | | | |  __/ (_| | | | (_| | |_) | |_| |
|_|\___|_| |_| |_|_| |_| |_|\___|\__, |_|  \__,_|_.__/ \__,_|
                                 |___/
------------------v1.1-----------------------------------------
""";
    print(banner);

def main():
    args=init_parser();
    if args.use_cookies:
        print('using firefox cookies');
    signal.signal(signal.SIGINT, signal_handler);
    show_banner();
    if args.username :
        try :
            num_downloader = 4;
            threads = [];
            username = args.username;
            lp = LinkProducer(username,num_downloader,args.use_cookies);
            lp.start();
            threads.append(lp);
            for i in range(0,num_downloader):
                download_worker = LinkProcessor(username);
                download_worker.start();
                threads.append(download_worker);
            for thread in threads:
                thread.join();
            print('all done stalker, everything stored in '+username+' folder');
        except requests.exceptions.ConnectionError as e:
            print('Connection error, check your network connection');
        except Exception as e :
            print(e);
    else:
        print('please specify username');

if __name__ == '__main__':
    main();
