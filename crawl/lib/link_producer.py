import random, time, json, requests, re, os
from .base_crawler import Base_Crawler
from .crawler_exceptions import *

class Link_Producer (Base_Crawler):
    __name = 'Producer ';
    __seq = 1;
    __base_url = 'https://www.instagram.com/';

    def __init__(self,username,num_downloader):
        super(Link_Producer,self).__init__();
        self.name = self.__name+str(Link_Producer.__seq);
        self.num_downloader = num_downloader;
        self.username = username;
        Link_Producer.__seq += 1;
        self.is_private(username);

    def get_seq(self):
        return Link_Producer.__seq;

    def grab_and_extract_data(self,link):
        raw = requests.get(link).content.decode('utf-8');
        match = re.findall('window._sharedData = (.*?);</script>',raw,re.DOTALL);
        return match[0];

    def get_raw_data(self,max_id):
        link = self.__base_url+self.username+'/?max_id='+max_id;
        return self.grab_and_extract_data(link);

    def get_video_data_url(self,code):
        return self.get_post_detail(code)['video_url'];

    def get_post_detail(self,code):
        link = self.__base_url+"p/"+code+"/";
        raw = self.decode_json(self.grab_and_extract_data(link));
        return raw['entry_data']['PostPage'][0]['media'];

    def has_next_page(self,list_data):
        return list_data['entry_data']['ProfilePage'][0]['user']['media']['page_info']['has_next_page'];

    def decode_json(self,raw_data):
        return json.loads(raw_data);

    def get_user_endpoint(self,data):
        if 'ProfilePage' not in data['entry_data']:
            raise no_account_exception;
        return data['entry_data']['ProfilePage'][0]['user'];

    def get_media_endpoint(self,data):
        return self.get_user_endpoint(data)['media'];

    def get_picts_from_slideshow(self,code):
        edges = self.get_post_detail(code)['edge_sidecar_to_children']['edges'];
        picts = [];
        for edge in edges:
            picts.append(edge['node']['display_url']);
        return picts;

    def set_termination_download_thread_flag(self):
        for i in range(0,self.num_downloader):
            self.get_queue().put(None);

    def is_private(self,username):
        if not self.get_user_endpoint(self.decode_json(self.get_raw_data('')))['is_private']:
            try:
                if not os.path.isdir('./'+username):
                    os.mkdir('./'+username,0o755);
            except Exception as e:
                print(e);
        else:
            self.set_termination_download_thread_flag();
            raise private_exception(username);

    def run(self):
        picts = [];
        raw_data=self.get_raw_data('');
        data = self.decode_json(raw_data);
        if self.get_media_endpoint(data)['count'] == 0:
            self.set_termination_download_thread_flag();
            raise zero_photo_exception;
        print('Crawling pictures from '+self.username);
        print('Total posts : '+ str(self.get_media_endpoint(data)['count']));
        print('please wait, gathering data...');
        display_picture = re.findall('(.*)s(.*)/(.*)',self.get_user_endpoint(data)['profile_pic_url_hd'],re.DOTALL)[0];
        self.get_queue().put(display_picture[0]+display_picture[2]);
        next_page = True;
        while next_page:
            last_link=''
            if(len(picts)>0):
                last_link = picts[len(picts)-1];
            data = self.decode_json(self.get_raw_data(last_link))
            for pict in self.get_media_endpoint(data)['nodes']:
                link = pict['display_src']
                if pict['is_video'] :
                    link=self.get_video_data_url(pict['code']);
                if pict['__typename'] == 'GraphSidecar':
                    for link in self.get_picts_from_slideshow(pict['code']):
                        self.get_queue().put(link);
                else:
                    self.get_queue().put(link);
                picts.append(pict['id']);
            next_page=self.has_next_page(data);
        self.set_termination_download_thread_flag();
