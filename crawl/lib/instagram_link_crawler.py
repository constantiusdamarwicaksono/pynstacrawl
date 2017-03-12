#!/usr/bin/python3
import os, requests, json, queue, re
from .crawler_exception import *

class instagram_link_crawler():

    __base_url = 'https://www.instagram.com/';

    #constructor, initialize instagram username
    def __init__(self,username):
        self.pict_links =  queue.Queue();
        self.username = username;
        print('crawling instagram for username : '+self.username);
    # getter for pict_links attribute
    def get_links(self):
        return self.pict_links;
    #capture raw data from instagram page
    def get_raw_data(self,username,max_id):
        link = self.__base_url+username+'/?max_id='+max_id;
        raw = requests.get(link).content.decode('utf-8');
        """using regex, capture the javascript line that contains juicy info"""
        match = re.findall('window._sharedData = (.*?);</script>',raw,re.DOTALL);
        return match[0];
    # get link from video post instead
    def get_video_data_url(self,code):
    	link = self.__base_url+"p/"+code+"/";
    	raw = requests.get(link).content.decode('utf-8');
    	match = re.findall('window._sharedData = (.*?);</script>',raw,re.DOTALL);
    	raw = self.decode_json(match[0]);
    	return raw['entry_data']['PostPage'][0]['media']['video_url'];
    #determine where the current page has more data, instagram only showing first 12 picts,
    def has_next_page(self,list_data):
    	return list_data['entry_data']['ProfilePage'][0]['user']['media']['page_info']['has_next_page'];
    #decode json
    def decode_json(self,raw_data):
    	return json.loads(raw_data);
    #get user endpoint of json data
    def get_user_endpoint(self,data):
        if 'ProfilePage' not in data['entry_data']:
            raise no_account_exception;
        return data['entry_data']['ProfilePage'][0]['user'];
    #get media endpoint of json data
    def get_media_endpoint(self,data):
        return self.get_user_endpoint(data)['media'];
    #main program
    def run(self):
        picts = [];
        """get initial data"""
        raw_data=self.get_raw_data(self.username,'');
        data = self.decode_json(raw_data);
        """green light if unprivate"""
        if self.get_user_endpoint(data)['is_private'] != True:
            if self.get_media_endpoint(data)['count'] == 0:
                raise zero_photo_exception;
            print('total pictures : '+ str(self.get_media_endpoint(data)['count']));
            print('please wait, gathering data...');
            next_page = True;
            while next_page:
                last_link=''
                if(len(picts)>0):
                    last_link = picts[len(picts)-1];
                data = self.decode_json(self.get_raw_data(self.username,last_link))
                for pict in self.get_media_endpoint(data)['nodes']:
                    link = pict['display_src']
                    if(pict['is_video']==True):
                        link=self.get_video_data_url(pict['code'])
                    self.pict_links.put(link);
                    picts.append(pict['id']);
                next_page=self.has_next_page(data);
            return self.pict_links;
        else:
            raise private_exception;

