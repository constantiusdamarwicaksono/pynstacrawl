class private_exception(Exception):
    def __init__(self):
        self.message  = 'this account is private';
        Exception.__init__(self,self.message);

class zero_photo_exception(Exception):
    def __init__(self):
        self.message = 'this account has 0 picts';
        Exception.__init__(self,self.message);

class no_account_exception(Exception):
    def __init__(self):
        self.message = 'no instagram account with supplied username';
        Exception.__init__(self,self.message);
