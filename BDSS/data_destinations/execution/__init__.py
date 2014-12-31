from abc import ABCMeta, abstractmethod

class JobExecutionError(Exception):
    pass

class BaseExecutionMethod():

    __metaclass__ = ABCMeta

    def __init__(self, destination_host, **kwargs):
        self.destination_host = destination_host
        for option, value in kwargs.iteritems():
            setattr(self, option, value)

    requires_ssh_key = False

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
