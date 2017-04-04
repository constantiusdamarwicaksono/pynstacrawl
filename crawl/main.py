#!/usr/bin/python3
"""
created by damar
"""
import sys, signal, requests
from lib.link_producer import Link_Producer
from lib.link_processor import Link_Processor

def signal_handler(signal, frame):
        print("\nAttempting to stop crawling process!!\n");
        sys.exit(0);

def main():
	signal.signal(signal.SIGINT, signal_handler);
	if len(sys.argv) > 1:
		try :
			num_downloader = 4;
			threads = [];
			username = sys.argv[1];
			lp = Link_Producer(username,num_downloader);
			lp.start();
			threads.append(lp);
			for i in range(0,num_downloader):
				download_worker = Link_Processor(username);
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
