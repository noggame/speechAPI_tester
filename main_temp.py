import time
from modules.Controller.TestController import TestController
from modules.Service.AnalysisManager import AnalyzerManager
from modules.Service.DataManager import DataManager, REG_DATA
from modules.Service.APIManager import ServiceManager, REG_SERVICE
from modules.Service.Type import SUPPORT

st = time.time()


### TestController init.
tc = TestController()


# TODO: static class 또는 singleton 으로 변경
M_Service = ServiceManager()
M_Data = DataManager()
M_Analyzer = AnalyzerManager()

print("초기화 = {}".format(time.time() - st))
st = time.time()


### Request API & DB
target = REG_DATA.AIHub
service = REG_SERVICE.KT
testResultList = tc.testWith(
    data=M_Data.findData(data_name=target.name, provider_name=target.value),            #     data=DM.findData(data_name="AIHub", provider_name="ETRI"),
    service_provider=M_Service.findServiceProvider(service_provider_name=service.name),    #     service_provider=SM.findServiceProvider(service_provider_name="KT"),
    analyzerInfo=M_Analyzer.findAnalyzer(support=SUPPORT.STT),
    support=SUPPORT.STT, #support=SUPPORT.STT,
    option={"limit":2})

if testResultList:
    print("샘플수 = {}, 평균_정확도 = {}".format(testResultList[0], round(testResultList[1],2)))
    
# print("종료 = {}".format(time.time() - st))

