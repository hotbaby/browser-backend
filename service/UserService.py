
import sys
from time import sleep
sys.path.insert(0, "../rpc")
sys.path.insert(0, "../interface/thrift/gen-py")

import logging
import multiprocessing
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TJSONProtocol, TBinaryProtocol, TCompactProtocol

from usr import User
from srvtracker import ServiceTracker
import srvtracker.ttypes
from IService import IService
from rpcthrift import ThriftRPCServer
from rpcthrift.ThriftRPCServer import ServerType
from rpcthrift.ThriftRPCServer import ProtocolType

logger = logging.getLogger("__main__")


class UserRPCServer(ThriftRPCServer.ThriftServer):
    """
    UserServiceServer comments.
    """

    def __init__(self,
                 host,
                 port,
                 server_type=ServerType.SIMPLE,
                 proto_type=ProtocolType.JSON):
        logger.info("Instance UserServiceServer")
        super(UserRPCServer, self).__init__(host, port, server_type, proto_type)
                
    def run(self):
        ThriftRPCServer.ThriftServer.run(self)

    def getService(self):
        return UserHandler()
    
    def getProcessor(self, handler):
        return User.Processor(handler)

    
class UserHandler(User.Iface):
    """
    UserHandler comments, inherit from User.Iface
    """
    
    def create(self, username, passwd):
        logger.debug("Invoke UserHandler.create method")
        return True
    
    def exist(self, username):
        logger.debug("Inovke UserHandler.exist metod")
        return True
    
    def update(self, username, passwd):
        logger.debug("Invoke UserHandler.update method")
        return True
    
    def remove(self, username):
        """
        delete is thrift reversed keyword and replaced with remove. 
        """
        logger.debug("Invoke UserHandler.remove method")
        return True

class RegisterException(Exception): pass
    

class UserService(IService):
    """
    UserService comments.
    """
    
    MAX_TRY_TIMES= 3
    
    def __init__(self,
                 sm_host,
                 sm_port=9000,
                 ptype=ProtocolType.JSON,
                 heartbeat_interval=5):
        self.sm_host = sm_host
        self.sm_port = sm_port
        self.ptype = ptype
        self.heartbeat_interval = heartbeat_interval
        self.rpc_server_process = None
        self.sm_client = None
        self.service_port = None
        self.service_id = None
        
        self.prepare()
    
    def prepare(self):
        self.connect_db()
        self.connect_sm()
        
    def run(self):
        #Register service to ServiceManager.
        try_times = 0
        while True:
            if try_times >= UserService.MAX_TRY_TIMES:
                logger.error("Register user service error.")
                raise RegisterException()
                assert(False)
                
            registry_resp = self.register()
            if not isinstance(registry_resp, srvtracker.ttypes.ServiceRegistryResponse):
                logger.error("Register response type error.")
                raise RegisterException()
            if registry_resp.result == 0:
                self.service_id = registry_resp.id
                self.service_port = registry_resp.port
                break
            else:
                try_times += 1
            
        self.start_rpc_server()
        #Send heartbeat message period
        while True:
            logger.debug("Send heartbeat message to service manager.")
            heartbeat_msg = srvtracker.ttypes.HeartbeatMessage(self.service_id)
            heartbeat_resp = self.sm_client.heartbeat(heartbeat_msg)
            if not isinstance(heartbeat_resp, srvtracker.ttypes.HeartbeatResponse):
                logger.error("Heartbeat reponse error.")
            sleep(self.heartbeat_interval)
    
    def get_protocol(self, transport):
        if self.ptype == ProtocolType.JSON:
            return TJSONProtocol.TJSONProtocol(transport)
        elif self.ptype == ProtocolType.BINARY:
            return TBinaryProtocol.TBinaryProtocol(transport)
        elif self.ptype == ProtocolType.COMPACT:
            return TCompactProtocol.TCompactProtocol(transport)
        else:
            return TJSONProtocol.TJSONProtocol(transport)
    
    def connect_sm(self):
        transport = TSocket.TSocket(self.sm_host, self.sm_port)
        transport = TTransport.TBufferedTransport(transport)
        proto = self.get_protocol(transport)
        self.sm_client = ServiceTracker.Client(proto)
        transport.open()
    
    def register(self):
        registry_info = srvtracker.ttypes.ServiceRegistryInfo(name="user",
                                                              host="0.0.0.0")
        return self.sm_client.register_service(registry_info)
    
    def connect_db(self): pass #TODO
    
    def start_rpc_server(self):
        if self.rpc_server_process == None:
            f = lambda host, port: UserRPCServer(host, port).run()
            self.rpc_server_process = multiprocessing.Process(target=f, args=("0.0.0.0", self.service_port))
            self.rpc_server_process.start()
        else: pass