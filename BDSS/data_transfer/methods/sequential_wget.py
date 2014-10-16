import os

from . import BaseTransferMethod

class SequentialWgetTransferMethod(BaseTransferMethod):

    def transfer_data(self, data_urls):
        for url in data_urls:
            os.system("wget --output-document=\"%s\" \"%s\"" % (self.output_path(url), url))
