from abc import ABC, abstractmethod

class ConverterBase(ABC):
    
    @abstractmethod
    @staticmethod
    def convert(rows, columns):
        '''should contain logic to accept rows and columns and return a data object for Azure.'''
        raise NotImplementedError