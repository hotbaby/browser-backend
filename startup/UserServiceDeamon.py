
import sys
sys.path.append("../")
sys.path.append("../rpc")
sys.path.append("../interface/thrift/gen-py")

import logging
from service.UserService import UserService


logger = logging.getLogger("__main__")

def main():
    user_service = UserService(sm_host="127.0.0.1")
    user_service.run()
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger.debug("Start Service Manager deamon.")
    main()
    