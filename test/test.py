import json
import  exceptions


class Super():
    
    def func(self):
        print("Call Super.func function")
        
class Derived(Super):
    
    def func(self):
        Super.func(self)
        
        
        
if __name__  == "__main__":
    d = dict(name="hello")
    if "name" in d:
        print(d["name"])
    else:
        print(None)
        
    