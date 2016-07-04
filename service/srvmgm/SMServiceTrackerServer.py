
import sys
from time import sleep
sys.path.insert(0, "../../rpc")
sys.path.insert(0, "../../interface/thrift/gen-py")

import logging

import rpcthrift
import srvtracker
from rpcthrift.ThriftRPCServer import ServerType, ProtocolType
    
from service.srvmgm.SMRegistry import RegistryProxy
from service.srvmgm.SMHeartbeat import HeartbeatProxy

logger = logging.getLogger("__main__")

__all__ = ["ServiceTrackerRPCServer"]


class ServiceTrackerRPCServer(rpcthrift.ThriftRPCServer.ThriftServer):
    """
    ServiceTrackerRPCServer comments.
    """
    
    def __init__(self,
                 heartbeat_queue,
                 service_registry,
                 host,
                 port,
                 server_type=ServerType.SIMPLE,
                 protocol_type=ProtocolType.JSON):
        super(ServiceTrackerRPCServer, self).__init__(host, port, server_type, protocol_type)
        self.heartbeat_queue = heartbeat_queue
        self.service_registry = service_registry
        logger.debug("Instance SrvMgmServer(host=%s,port=%d, server_type=%s, protocol_type=%s)."
                      % (host, port, server_type, protocol_type))
    
    def run(self):
        super(ServiceTrackerRPCServer, self).run()
        
    def getService(self):
        return ServiceTrackerHandler(self.heartbeat_queue,
                                     self.service_registry)
        
    def getProcessor(self, handler):
        return srvtracker.ServiceTracker.Processor(handler)


class ServiceTrackerHandler(srvtracker.ServiceTracker.Iface):
    """
    ServiceTrackerHandler comments
    """
    
    def __init__(self, heartbeat_queue, service_registry):
        self.heartbeat_queue = heartbeat_queue
        self.service_registry = service_registry
        
    def register_service(self, info):
        logger.debug("Process register_service.")
        proxy = RegistryProxy(self.service_registry)
        return proxy.register_service(info)
    
    def heartbeat(self, msg):
        logger.debug("Process heartbeat.")
        proxy = HeartbeatProxy(self.heartbeat_queue)
        return proxy.heartbeat(msg)
    
    def get_service(self, name):
        logger.debug("Process get_service")
        proxy = RegistryProxy(self.service_registry) 
        return proxy.get_service(name)
        
    def get_services(self):
        logger.debug("Received get_services.")
        #TODO