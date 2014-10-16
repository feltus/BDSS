from abc import ABCMeta, abstractmethod

class BaseGrouping():
    __metaclass__ = ABCMeta

    ## Split a job's data items into groups. The transfer of each group
    #  will be handled by a different process.
    #  @param data_urls Collection of URLs.
    #  @return Collection of collections of URLs. Each collection should
    #   contain the URLs that will be grouped together.
    @abstractmethod
    def group_urls(self, data_urls):
        pass
