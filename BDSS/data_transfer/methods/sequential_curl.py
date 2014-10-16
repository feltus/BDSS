import os

from . import BaseTransferMethod

class SequentialCurlTransferMethod(BaseTransferMethod):

    def transfer_data(self, data_urls):
        for url in data_urls:
            os.system("curl --output \"%s\" \"%s\"" % (self.output_path(url), url))
