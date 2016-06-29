
import logging
import Queue

logger = logging.getLogger("__main__")

__all__ = ["ServiceExceptionReport"]


class ServiceExceptionReport(object):
    """
    ServiceExceptionReport comments.
    """
    
    EXCEPTION_QUEUE = Queue.Queue() 
    
    def __init__(self): pass
    
    def prepare(self): pass
        
    def report(self): pass
    
    @classmethod
    def putException(cls, exception):
        ServiceExceptionReport.EXCEPTION_QUEUE.put_nowait(exception)