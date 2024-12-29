from abc import ABC, abstractmethod

class ReaderBase(ABC):

    # setup up variables in __init__
    configs = None

    def __init__(self, *args, **kwargs):
        '''Should validate and prepare the configs necassary for connecting to Data Source.'''
        raise NotImplementedError

    @abstractmethod
    def read(self, query):
        '''Should connect to Data source using params from instance and return the rows and columns in the Data source.'''
        raise NotImplementedError