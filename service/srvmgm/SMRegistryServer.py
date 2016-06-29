
import sys
sys.path.insert(0, "../../rpc")
sys.path.insert(0, "../../interface/thrift/gen-py")

import logging
import srvtracker.ttypes
import srvtracker.ServiceTracker


logger = logging.getLogger("__main__")

__all__ = ["RegistryServer", "RegistryProxy"]


GLOBAL_SERVICE_COUNT = 0
GLOBAL_SERVICE_PORT_INDEX = 9001

class RegistryServer(object):
    """
    Service comments.
    """
    
    def __init__(self, service_registry):
        self.service_registry = service_registry

    def register(self, service_info):
        if isinstance(service_info, srvtracker.ttypes.ServiceRegistryInfo):
            global GLOBAL_SERVICE_COUNT, GLOBAL_SERVICE_PORT_INDEX
            service_id = GLOBAL_SERVICE_COUNT
            GLOBAL_SERVICE_COUNT += 1
            service_port = GLOBAL_SERVICE_PORT_INDEX
            GLOBAL_SERVICE_PORT_INDEX += 1
            service_profile = srvtracker.ttypes.ServiceProfile(service_id,
                                                               service_info.name,
                                                               service_info.host,
                                                               service_port)
            # Override if the service name has existed.
            self.service_registry[service_info.name] = service_profile
            return srvtracker.ttypes.ServiceRegistryResponse(result=0, id=service_id, port=service_port)
        else:
            return srvtracker.ttypes.ServiceRegistryResponse(result=-1, id=-1, port=-1)
        
    def get_service(self, name):
        if name in self.service_registry:
            return srvtracker.ttypes.ServiceProfile(-1, "", "", -1)
        else:
            return self.service_registry[name]


class RegistryProxy(srvtracker.ServiceTracker.Iface):
    """
    ServiceRegisterProxy comments.
    """
    
    def __init__(self, service_registry):
        self.service_registry = service_registry
        
    def register_service(self, info):
        registry = RegistryServer(self.service_registry)
        return registry.register(info)
    
    def get_services(self): pass
    
    def get_service(self, name):
        registry = RegistryServer(self.service_registry)
        return registry.get_service(name)