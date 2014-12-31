from abc import ABCMeta, abstractmethod

class FileTransferError(Exception):
    pass

class BaseFileTransferMethod():

    __metaclass__ = ABCMeta

    requires_ssh_key = False

    def __init__(self, destination_host, **kwargs):
        self.destination_host = destination_host
        for option, value in kwargs.iteritems():
            setattr(self, option, value)

    ## Open connection to destination.
    @abstractmethod
    def connect(self):
        pass

    ## Create a directory tree on the destination host.
    #  @param dir_path The absolute path to create.
    @abstractmethod
    def mkdir_p(self, dir_path):
        pass

    ## Transfer job file to destination.
    #  @param dest_file_path The path to save the file to on the remote host.
    #   This path is relative to the remote host's base directory for BDSS jobs.
    #  @param file_data The data for a file.
    @abstractmethod
    def transfer_file(self, dest_file_path, file_data):
        pass

    ## Disconnect from destination.
    @abstractmethod
    def disconnect(self):
        pass
