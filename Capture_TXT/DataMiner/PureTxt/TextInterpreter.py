import pandas as pd
import abc

class TextInterpreter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create_df(self, text:str, name_type:str):
        """Extract the information into text and convert it into a data frame"""
        pass
