import abc

class Data(metaclass=abc.ABCMeta): 
    """Super class for the different types of data we want for mongodb"""

    def __init__(self): 
        """Simply assigns the name of the class to the value for data"""
        self.data = self.__class__.__name__ #This allows all inherited class to have a self.data value that is their class name

    @abc.abstractmethod
    def to_dictionary(self):
        """This is intended for the purpose of making sure that there is a 
        way to convert the classes into the dictionaries that we will be putting into
        mongoDB"""
        pass