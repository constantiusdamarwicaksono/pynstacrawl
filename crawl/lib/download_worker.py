#!/usr/bin/python3
import threading, time, queue, requests, os

class download_worker(threading.Thread):
	#use __ to hide data, e.g. __que, __exit_flag
	que = queue.Queue();
	__exit_flag=0;
	__thread_lock = threading.Lock();
	def __init__(self,t_name,t_delay,_dir):
		threading.Thread.__init__(self);
		self.name = t_name;
		self.delay = t_delay;
		self.dir = _dir;
		# print('creating thread ' +  self.name);
	def run(self):
		while not self.__exit_flag:
			#print(self.name+' status '+str(self.isAlive()));
			if not download_worker.que.empty():
				self.__thread_lock.acquire();
				link =  download_worker.que.get();
				self.__thread_lock.release();
				print(self.name+' running on '+ str(link));
				self.download_file(self.dir,link[link.rfind('/')+1:],link);
			else:
				self.__exit_flag=1;
			# time.sleep(self.delay);
	def download_file(self,dir,name,link):
		if not os.path.isfile('./'+dir+'/'+name):
			try:
				r = requests.get(link);
				with open('./'+dir+'/'+name,'wb') as outfile:
					outfile.write(r.content);
				outfile.close();
				#urllib.request.urlretrieve(link, './'+username+'/'+file_name)
				# print(' -> downloaded')
				return True
			except:
				return False
		else:
			# print(' -> not downloaded')
			return False
