
from typing import List


class APICaller:
    def __init__(self, url, key, targetFile=None, options=None) -> None:
        self._url = url
        self._key = key
        self._targetFile = targetFile
        self._options = options

    @property
    def url(self):
        return self._url

    @property
    def key(self):
        return self._key

    @property
    def options(self):
        return self._options

    @property
    def targetFile(self):
        return self._targetFile

    @url.setter
    def url(self, url):
        self._url = url

    @key.setter
    def key(self, key):
        self._key = key

    @options.setter
    def options(self, options):
        self._options = options

    @targetFile.setter
    def targetFile(self, targetFile):
        self._targetFile = targetFile

    def request(self, url, key, targetFile, options=None) -> List:
        result = [str]

        # update params.
        self.url = url if not url else self.url
        self.key = key if not key else self.key
        self.options = options if not options else self.options
        self.targetFile = targetFile if not targetFile else self.targetFile
        
        # implements

        return result