
import sys
sys.path.insert(0, "../interface/thrift/gen-py")

import logging
import unittest
from userservice import User

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TJSONProtocol

logger = logging.getLogger("__main__")

class TestUserService(unittest.TestCase):
    """
    TestUserService comments
    """
    
    def setUp(self):
        transport = TSocket.TSocket("localhost", 9000)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TJSONProtocol.TJSONProtocol(transport)
        self.client = User.Client(protocol)
        self.trans = transport
        transport.open()
        
    def tearDown(self):
        self.trans.close()
        
    def testCreate(self):
        logger.debug("Test UserService.create")
        result = self.client.create("username", "passwd")
        self.assertTrue(result, "Test UserService.create Error")

    def testRemove(self):
        logger.debug("Test UserService.remove")
        result = self.client.remove("username")
        self.assertTrue(result, "Test UserService.remove Error")
     
    def testUpdate(self):
        logger.debug("Test UserService.update")
        result = self.client.update("username", "passwd")
        self.assertTrue(result, "Test UserService.update Error")
        
    def testExist(self):
        logger.debug("Test UserService.exist")
        result = self.client.exist("username")
        self.assertTrue(result, "Test UserService.exist Error")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger.info("Test UserService functions")
    unittest.main()