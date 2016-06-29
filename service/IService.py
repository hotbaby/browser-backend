from abc import abstractmethod

__all__ = ["IService"]

class IService(object):
    """
    Abstract the Service API.
    """
    
    @abstractmethod
    def connect_db(self): pass
    "Connect to the database"
    
    @abstractmethod
    def register(self): pass
    """
    Register service to ServiceManager.
    Must be realized by Derived class.
    """
    
    @abstractmethod
    def heartbeat(self): pass
    """
    Send heartbeat to ServiceManager.
    Must be realized by the Derived class.
    """
    
    @abstractmethod
    def start_rpc_server(self): pass
    """
    Start RPC(thrift) Server. 
    Should be run rpc server in a special process.
    Must be realized by the Derived class.
    """
    
    @abstractmethod
    def run(self): pass
    """
    Start run service.
    Must be realized by the Derived class.
    """