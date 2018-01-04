class PrivateException(Exception):
    def __init__(self,username):
        self.message  = 'sorry, but this account ('+username+') is private';
        Exception.__init__(self,self.message);

class ZeroPhotoException(Exception):
    def __init__(self):
        self.message = 'this account has 0 picts';
        Exception.__init__(self,self.message);

class NoAccountException(Exception):
    def __init__(self):
        self.message = 'no instagram account with supplied username';
        Exception.__init__(self,self.message);
