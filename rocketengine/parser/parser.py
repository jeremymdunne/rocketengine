import os.path
from . import raspparser

def parseEngineFile(filepath):
    # look at the extension to determine which parser to use
    extension = os.path.splitext(filepath)[1]
    if '.eng' in extension:
        return raspparser.parseRaspFile(filepath)
    else:
        pass
        #TODO throw exceptions
