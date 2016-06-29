
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
            service_profile = srvtracker.ttypes.ServiceProfile(service_info, service_id)
            # Override if the service name has existed.
            self.service_registry[service_info.name] = service_profile
            service_port = GLOBAL_SERVICE_PORT_INDEX
            GLOBAL_SERVICE_PORT_INDEX += 1
            return srvtracker.ttypes.ServiceRegistryResponse(result=0, id=service_id, port=service_port)
        else:
            return srvtracker.ttypes.ServiceRegistryResponse(result=-1, id=-1, port=-1)


class RegistryProxy(srvtracker.ServiceTracker.Iface):
    """
    ServiceRegisterProxy comments.
    """
    
    def __init__(self, service_registry):
        self.service_registry = service_registry
        
    def register_service(self, info):
        registry = RegistryServer(self.service_registry)
        return registry.register(info)