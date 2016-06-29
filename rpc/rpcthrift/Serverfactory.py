import logging

from thrift.server import TNonblockingServer
from thrift.server import TServer
from thrift.server import TProcessPoolServer
from thrift.transport import TSocket
from thrift.transport import TTransport

logger = logging.getLogger("__main__")

__all__ = ["TServerCustomerFactory"]

class IServerFactory(object):
    
    def buildServer(self):
        pass
    

class TServerCustomerFactory(object):
        
    @classmethod
    def buildNoblockingServer(cls,
                              host,
                              port,
                              processor,
                              pfactory):
        logger.debug("build Thrift Nonblocking Server")
        transport = TSocket.TServerSocket(host=host, port=port)
        return TNonblockingServer.TNonblockingServer(processor, transport, inputProtocolFactory=pfactory)
    
    @classmethod
    def buildSimpleServer(cls,
                          host,
                          port,
                          processor,
                          pfactory):
        logger.debug("build Thrift Simple Server")
        transport = TSocket.TServerSocket(host=host, port=port)
        tfactory = TTransport.TBufferedTransportFactory()
        return TServer.TSimpleServer(processor, transport, tfactory, pfactory)
    
    @classmethod
    def buildPoolServer(cls,
                        host,
                        port,
                        processor,
                        pfactory):
        logger.debug("Build Thrift Processor Pool Server")
        transport = TSocket.TServerSocket(host=host, port=port)
        tfactory = TTransport.TBufferedTransportFactory()
        return TProcessPoolServer.TProcessPoolServer(processor, transport, tfactory, pfactory)