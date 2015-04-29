
__author__ = "victor"
__date__ = "$26/04/2015 06:15:38$"

import hashlib as hash

class MD5():
    
    def __init__(self, key):
        self.key = key
        self.md5 = None
    
    def calc(self):
        if not self.md5:
            m = hash.md5()
            m.update(self.key)
            self.md5 = m.hexdigest()
        return self.md5
    
    def compare(self, keyToSee):
        return self.calc() == keyToSee
    
    def __eq__(self,m):
        return self.key == m.key
    
    def __repr__(self):
        self.calc()
        return "|{:^10} | {:^40}|".format(self.key, self.md5)
