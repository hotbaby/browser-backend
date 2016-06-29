import json
import  exceptions


class Super():
    
    def func(self):
        print("Call Super.func function")
        
class Derived(Super):
    
    def func(self):
        Super.func(self)
        
        
        
if __name__  == "__main__":
    index = 1;
    