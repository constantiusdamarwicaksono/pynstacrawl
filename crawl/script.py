#!/usr/bin/python3
import urllib.request
import re
import sys
import json
import argparse
import os

def sayhello(string):
	print('hello '+string)

def get_video_data_url(code):
	link = "https://www.instagram.com/p/"+code+"/"
	f = urllib.request.urlopen(link)
	raw = f.read().decode('utf-8')
	match = re.findall('window._sharedData = (.*?);</script>',raw,re.DOTALL)
	f.close()
	raw = decode_json(match[0])
	return raw['entry_data']['PostPage'][0]['media']['video_url']

def get_raw_data(username,max_id):
	link = "https://www.instagram.com/"+username+'/?max_id='+max_id
	# print(link)
	f = urllib.request.urlopen(link)
	raw = f.read().decode('utf-8')
	match = re.findall('window._sharedData = (.*?);</script>',raw,re.DOTALL)
	f.close()
	return match[0]

def has_next_page(list_data):
	return list_data['entry_data']['ProfilePage'][0]['user']['media']['page_info']['has_next_page']

def decode_json(raw_data):
	return json.loads(raw_data)

def download_file(link,file_name,username):
	if not os.path.isdir('./'+username):
		os.mkdir('./'+username,0o775)
	if not os.path.isfile('./'+username+'/'+file_name):
		try:
			urllib.request.urlretrieve(link, './'+username+'/'+file_name)
			print(' -> downloaded')
			return True
		except:
			return False
	else:
		print(' -> not downloaded')
		return False

#parser = argparse.ArgumentParser('Hello stalker')
#parser.add_argument('-u',help='instagram username account you want to stalk')
#args = parser.parse_args()
#print(args.u)

if len(sys.argv)>1 :
	picts = []
	sayhello('stupid')
	username = sys.argv[1]
	print('instagram account for',username)
	raw_data=get_raw_data(username,'')
	data = decode_json(raw_data)
	if(data['entry_data']['ProfilePage'][0]['user']['is_private']!=True):
		print('total pictures : '+ str(data['entry_data']['ProfilePage'][0]['user']['media']['count']))
		print('picture links :')
		next_page = True
		while next_page:
			last_link=''
			if(len(picts)>0):
				last_link = picts[len(picts)-1];
			data = decode_json(get_raw_data(username,last_link))
			for pict in data['entry_data']['ProfilePage'][0]['user']['media']['nodes']:
				link = pict['display_src']
				if(pict['is_video']==True):
					link=get_video_data_url(pict['code'])
				match = re.findall('(.*)s750x750/sh0.08/e35/(.*)',link,re.DOTALL)
				if(len(match)>0):
					print(match[0][0]+match[0][1],end='')
				else:
					print(link,end='')
				file_name = link[link.rfind('/')+1:]
				download_file(link,file_name,username)
				picts.append(pict['id'])
			next_page=has_next_page(data);
		print('All done stalker !, everything downloaded at '+ username +' folder')
	else:
		print('sorry, private account')


else :
	print('please input an instagram username')
