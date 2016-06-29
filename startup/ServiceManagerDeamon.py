
import sys
sys.path.append("../")
sys.path.append("../rpc")
sys.path.append("../interface/thrift/gen-py")

import logging
from service.srvmgm import ServiceManager 


logger = logging.getLogger("__main__")

def main():
    sm = ServiceManager.ServiceManager()
    sm.run()
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger.debug("Start Service Manager deamon.")
    main()
    