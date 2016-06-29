import sys
sys.path.insert(0, "../../rpc")
sys.path.insert(0, "../../interface/thrift/gen-py")

import logging

import srvtracker.ServiceTracker
import ServiceManager

logger = logging.getLogger("__main__")

__all__ = ["HeartbeatServer", "HeartbeatProxy"]


class HeartbeatServer(object):
    """
    HeartbeatServer comments.
    """

    def __init__(self, msg_queue):
        self.msg_queue = msg_queue
        
    def process_heartbeat_message(self):
        try:
            msg = self.msg_queue.get_nowait()
            if isinstance(msg, srvtracker.ttypes.HeartbeatMessage):
                logger.debug("Process (service %d) heartbeat message." % msg.service_id)
                pass #TODO process heartbeat message.
        except Exception:
            logger.info("Heartbeat queue is empty.")
        
        
    @classmethod
    def put_msg(cls, queue, msg):
        if not isinstance(msg, srvtracker.ttypes.HeartbeatMessage):
            logger.warn("heartbeat message format error.")
            return False
        else:
            try:
                queue.put_nowait(msg)
                ServiceManager.increase_semaphore()
                return True
            except Exception:
                logger.warn("Put msg into HEARTBEAT_QUEUE error.")
                return False


class HeartbeatProxy(srvtracker.ServiceTracker.Iface):
    """
    HeartbeatProxy comments.
    """

    def __init__(self, msg_queue):
        self.msg_queue = msg_queue
        
    def heartbeat(self, msg):
        if not isinstance(msg, srvtracker.ttypes.HeartbeatMessage):
            logger.warn("hesartbeat message format error.")
            return srvtracker.ttypes.HeartbeatResponse(result=-1)
        else:
            HeartbeatServer.put_msg(self.msg_queue, msg)
            return srvtracker.ttypes.HeartbeatResponse(result=0)