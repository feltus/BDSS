from os import makedirs, path

from . import BaseFileTransferMethod

class LocalFileTransferMethod(BaseFileTransferMethod):

    def connect(self):
        pass

    def mkdir_p(self, dir_path):
        if not path.exists(dir_path):
            makedirs(path.expandvars(path.expanduser(dir_path)))

    def transfer_file(self, dest_file_path, file_data):
        file = open(path.expandvars(path.expanduser(dest_file_path)), 'w')
        file.write(file_data)
        file.close()

    def disconnect(self):
        pass
