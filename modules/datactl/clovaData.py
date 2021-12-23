import logging
import json

class ClovaDataController:
    def __init__(self, baseDir=None, answer=None) -> None:
        self._baseDir = baseDir
        self._answer = answer

    @property
    def baseDir(self):
        return self._baseDir

    @property
    def answer(self):
        return self._answer
    
    @baseDir.setter
    def baseDir(self, baseDir):
        self._baseDir = str(baseDir)

    @answer.setter
    def answer(self, answer):
        self._answer = str(answer)

    def getExpectedList(self):
        try:
            target = open(f'{self._baseDir}/{self._answer}', 'r').readline()
        except FileNotFoundError:
            logging.exception(f'{self._baseDir}/{self._answer} file not found.')

        return json.loads(target)