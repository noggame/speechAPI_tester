import config.cfgParser as cfg
from modules.Service.Type import SUPPORT
from modules.Service.Data.BaseDataParser import BaseDataParser
from modules.Service.Data.DataParser.STT.AIHubParser import AIHubParser
from modules.Service.Data.DataParser.STT.ClovaAIParser import ClovaAIParser
from enum import Enum

class ParserInfo():
    def __init__(self, parser:BaseDataParser, support:SUPPORT) -> None:
        self.parser = parser
        self.support = support


class DataInfo():
    def __init__(self, name, provider, path) -> None:
        self.name = name
        self.provider = provider
        self.path = path
        self.parserList = []

    def addParser(self, parser:ParserInfo):
        if parser:
            self.parserList.append(parser)

    def findParser(self, support:SUPPORT):
        for parser in self.parserList:
            parser:ParserInfo = parser
            if parser.support == support:
                return parser
        return None


class DataManager():
    def __init__(self) -> None:
        self.dataList = []

        # AIHub
        AIHub = DataInfo(name="AIHub", provider="ETRI", path=cfg.get("data", "AIHub"))
        AIHub.addParser(ParserInfo(
            parser=AIHubParser(targetPath=AIHub.path),
            support=SUPPORT.STT))
        self.dataList.append(AIHub)

        # ClovaAI
        ClovaAI = DataInfo(name="ClovaAI", provider="Naver", path=cfg.get("data", "ClovaAI"))
        ClovaAI.addParser(ParserInfo(
            parser=ClovaAIParser(targetPath=ClovaAI.path),
            support=SUPPORT.STT))
        self.dataList.append(ClovaAI)

    def findData(self, data_name:str, provider_name:str) -> DataInfo:
        for data in self.dataList:
            data:DataInfo = data
            if data.name == data_name and data.provider == provider_name:
                return data
        return None


class REG_DATA(Enum):
    # DATA_NAME & PROVIDER
    AIHub = "ETRI"
    ClovaAI = "Naver"