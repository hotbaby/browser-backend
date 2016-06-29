
import sys
sys.path.insert(0, "../../rpc")

import logging
import multiprocessing

from rpcthrift import ThriftRPCServer

from service.srvmgm.SMServiceTrackerServer import ServiceTrackerRPCServer
from service.srvmgm.SMHeartbeatServer import HeartbeatServer

logger = logging.getLogger("__main__")

__all__ = ["ServiceManager", "increase_semaphore"]


class ServiceManager(object):
    """
    ServiceManager comments.
    """
    
    HEARTBEAT_QUEUE = multiprocessing.Queue()
    SERVICE_REGISTRY = dict()
    SEMAPHORE = multiprocessing.Semaphore(value=0)
    
    def __init__(self,
                 host="0.0.0.0",
                 port=9000,
                 server_type = ThriftRPCServer.ServerType.SIMPLE,
                 protocol_type = ThriftRPCServer.ProtocolType.JSON):
        self.host = host
        self.port = port
        self.server_type = server_type
        self.protoco_type = protocol_type
        self.rpc_server_process = None
        self.prepare()
        
    def prepare(self):
        self.heartbeat = HeartbeatServer(ServiceManager.HEARTBEAT_QUEUE)
        
    def run(self):
        self.start_rpc_server()
        while True:
            ServiceManager.SEMAPHORE.acquire()
            self.heartbeat.process_heartbeat_message()
    
    def start_rpc_server(self):
        if self.rpc_server_process == None:
            rpc_server_func = lambda q, registry, host, port, stype, ptype:\
                                    ServiceTrackerRPCServer(q, registry, host, port, stype, ptype).run() 
            self.rpc_server_process = multiprocessing.Process(target=rpc_server_func,
                                                              args=(ServiceManager.HEARTBEAT_QUEUE,
                                                                    ServiceManager.SERVICE_REGISTRY,
                                                                    self.host,
                                                                    self.port,
                                                                    self.server_type,
                                                                    self.protoco_type))
            self.rpc_server_process.start()
        else: pass


def increase_semaphore():
    ServiceManager.SEMAPHORE.release()