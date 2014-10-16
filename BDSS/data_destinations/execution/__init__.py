from abc import ABCMeta, abstractmethod

class BaseExecutionMethod():

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        for option, value in kwargs.iteritems():
            setattr(self, option, value)

    ## Open connection to destination.
    @abstractmethod
    def connect(self):
        pass

    ## Execute job script.
    @abstractmethod
    def execute_job(self, working_directory):
        pass

    ## Disconnect from destination.
    @abstractmethod
    def disconnect(self):
        pass
