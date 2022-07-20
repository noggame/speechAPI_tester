import time
import logging
from Struct.Result import TestResult
from modules.Controller.TestController import TestController
from modules.Service.APICaller.BaseAPICaller import BaseAPICaller
from modules.Service.DataParser.BaseDataParser import BaseDataParser
from modules.Service.ResultAnalyzer.Vision.FDResultAnalyzer import FDResultAnalyzer
from modules.Service.Type import SERVICE_TYPE
from modules.DesignPattern.Factory import DataParserFactory as df, ServiceFactory as sf, AnlalyzerFactory as af
import json

tc = TestController()

cur_time = time.time()
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

f = open("/Users/songdonghun/workspace/python/speechAPI_tester/logs/eval.txt", "r")

resultList = []
for line in f.readlines():
    jd:dict = json.loads(line)

    tr = TestResult(id = jd.get("id"),
                source = jd.get("source"),
                service = jd.get("service"),
                expected = jd.get("expected"),
                actual = jd.get("actual"))
    
    resultList.append(tr)

fa = FDResultAnalyzer()
fa.analysisResultStack(resultList)


logging.info("[총 소요시간] : {}".format(time.time()-cur_time))
