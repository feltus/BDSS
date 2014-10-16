from . import BaseGrouping

class NoGrouping(BaseGrouping):

    def group_urls(self, data_urls):
        return [data_urls]
