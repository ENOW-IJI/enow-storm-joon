import sys
import threading
import json
import codecs
import logging
import os
from time import sleep

'''
    List : Global Variables
    Descriptions :
    threadExit : A variable for detecting whether a thread executing the body source has exited"
    loggerStdout : A variable logging the stream passed out on STDOUT
    loggerStderr : A variable logging the stream passed out on STDERR
    lock = A semaphore assigned from thread
    '''

def kilobytes(megabytes):
    return megabytes * 1024 * 1024

def eventHandlerFacade(_event, _context, _callback, _mapId_hashed_string, _modulePath):
    mapId_hashed_string = os.path.join(_modulePath, _mapId_hashed_string)
    sys.path.append(_modulePath)
    sys.path.append(mapId_hashed_string)
    import body
    from body import eventHandler
    from StreamToLogger import StreamToLogger
    
    loggerStdoutFilePath = os.path.join(mapId_hashed_string, 'log', 'log.txt')
    
    logging.basicConfig(
                        level=logging.DEBUG,
                        format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
                        filename=loggerStdoutFilePath,
                        filemode='a'
    )
        
    stdout_logger = logging.getLogger('STDOUT')
    sl = StreamToLogger(stdout_logger, logging.INFO)
    sys.stdout = sl
                        
    stderr_logger = logging.getLogger('STDERR')
    sl = StreamToLogger(stderr_logger, logging.ERROR)
    sys.stderr = sl
    
    try:           
        eventHandler(_event, _context, _callback)
    except Exception as e:
        sys.exit()


def Main():
    
    jsonDump = ""
    parameterDump = ""
    previousDataDump = ""
    mapId_hashed_string = ""
    pathDump = ""
    _event = None
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    while True:
        binaryString = sys.stdin.readline()
        
        if not binaryString:
            break
        
        if binaryString == b"endl\n":
            break
        
        jsonDump += codecs.encode(binaryString, 'utf-8')

    while True:
        binaryString = sys.stdin.readline()
        
        if not binaryString:
            break
        
        if binaryString == b"endl\n":
            break
        
        parameterDump += codecs.encode(binaryString, 'utf-8')

    while True:
        binaryString = sys.stdin.readline()
        
        if not binaryString:
            break

        if binaryString == b"endl\n":
            break
        
        previousDataDump += codecs.encode(binaryString, 'utf-8')

    while True:
        binaryString = sys.stdin.readline()
        
        if not binaryString:
            break

        if binaryString == b"endl\n":
            break
        
        mapId_hashed_string += codecs.encode(binaryString, 'utf-8')

    while True:
        binaryString = sys.stdin.readline()
        
        if not binaryString:
            break

        if binaryString == b"endl\n":
            break
        
        pathDump += codecs.encode(binaryString, 'utf-8')

    jsonDump = jsonDump.replace("\n", "")
    parameterDump = parameterDump.replace("\n", "")
    previousDataDump = previousDataDump.replace("\n", "")
    mapId_hashed_string = mapId_hashed_string.replace("\n", "")
    pathDump = pathDump.replace("\n", "")
    
    modulePath = os.path.join(pathDump, "enow/jython/pythonSrc")
    sys.path.append(modulePath)
    
    from postCode import postProcess
    
    if jsonDump != "null":
        _event = json.loads(jsonDump)
    _context = dict()
    _callback = dict()
    _previousData = json.loads(previousDataDump)
    
    """
        context object written in json
        ATTRIBUTES:
        * function_name
        * function_version
        * invoked_ERN
        * memory_limit_in_mb
        """
    _context["function_name"] = ""
    _context["function_version"] = ""
    _context["invoked_ERN"] = ""
    _context["memory_limit_in_mb"] = 64
    _context["topicName"] = ""
    _context["deviceID"] = ""
    _context["parameter"] = parameterDump
    _context["previousData"] = _previousData
    
    """
        setting up a thread for executing a body code
        """
    thread_running = threading.Thread(name="Running", target=eventHandlerFacade, kwargs={'_event' : _event, '_context' : _context, "_callback" : _callback, '_mapId_hashed_string' : str(mapId_hashed_string), '_modulePath' : modulePath })
    
    thread_running.start()
    thread_running.join()
    
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    
    _event = json.loads("{ \"job\" : \"completed\" }")
    _context["previousData"] = ""
    postProcess(_event, _context, _callback)

if __name__ == "__main__":
    '''
        sys.stderr.write("preCode.py : running")
        sys.stderr.flush()
    '''
    Main()
    '''
        sys.stderr.write("preCode.py : exiting")
        sys.stderr.flush()
    '''
