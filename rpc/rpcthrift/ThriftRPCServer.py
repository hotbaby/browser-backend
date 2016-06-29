import logging

from thrift.protocol import TJSONProtocol, TBinaryProtocol, TCompactProtocol
from Serverfactory import TServerCustomerFactory

logger = logging.getLogger("__main__")

__all__ = ["ThriftServer", "ServerType", "ProtocolType"]


class ProtocolType(object):
    """
    ProtocolType comments
    """
    BINARY  = "binary"
    JSON    = "json"
    COMPACT =  "compact"
    
    
class ServerType(object):
    """
    ServertType comments 
    """
    
    NOBLOCKING  = "noblocking"
    SIMPLE      = "simple"
    POOL        = "pool"

    
class ThriftServer(object):
    """
    ThriftServer comments
    """

    def __init__(self,
                 host, 
                 port,
                 serverType=ServerType.SIMPLE,
                 protocolType=ProtocolType.JSON):
        self.host = host
        self.port = port
        self.serverType = serverType
        self.protocolType = protocolType
        self.server = None
        
    def run(self):
        if self.server == None:
            if self.serverType == ServerType.NOBLOCKING:
                self.server = TServerCustomerFactory.buildNoblockingServer(self.host,
                                                                           self.port,
                                                                           self.getProcessor(self.getService()),
                                                                           self.getProtocolFactory())
            elif self.serverType == ServerType.SIMPLE:
                self.server = TServerCustomerFactory.buildSimpleServer(self.host,
                                                                       self.port,
                                                                       self.getProcessor(self.getService()),
                                                                       self.getProtocolFactory())
            elif self.serverType == ServerType.POOL:
                self.server = TServerCustomerFactory.buildPoolServer(self.host,
                                                                     self.host,
                                                                     self.getProcessor(self.getService()),
                                                                     self.getProtocolFactory())
            else:
                self.server = TServerCustomerFactory.buildSimpleServer(self.host,
                                                                       self.port,
                                                                       self.getProcessor(self.getService()),
                                                                       self.getProtocolFactory())
            self.server.serve()
        else: pass
    
    def getService(self): pass
    """
    Get service concrete handler instance.
    MUST be realize by Derived Class.
    """
    
    def getProcessor(self, handler): pass
    """
    Get service processor instance.
    MUST be realize by Derived Class. 
    """
        
    def getProtocolFactory(self):
        if self.protocolType == ProtocolType.JSON:
            return TJSONProtocol.TJSONProtocolFactory()
        elif self.protocolType == ProtocolType.BINARY:
            return TBinaryProtocol.TBinaryProtocolFactory()
        elif self.protocolType == ProtocolType.COMPACT:
            return TCompactProtocol.TCompactProtocolFactory()
        else:
            return TJSONProtocol.TJSONProtocolFactory()