import time
from modules.Controller.TestController import TestController
from modules.Service.APICaller.BaseAPICaller import BaseAPICaller
from modules.Service.DataParser.BaseDataParser import BaseDataParser
from modules.Service.Type import SERVICE_TYPE
from modules.DesignPattern.Factory import DataParserFactory as df, ServiceFactory as sf, AnlalyzerFactory as af

tc = TestController()

cur_time = time.time()

########## Face
# tc = TestController()
test_option = {
    'data_limit' : 100,
    'update_data' : True
}
### STT
# testResultList = tc.testWith(testdata = df.DATA_NAME.__getitem__(name="ClovaAI"),
#                         service_provider = sf.PROVIDER.__getitem__(name="KT"),
#                         service_type = SERVICE_TYPE.__getitem__(name="STT"),
#                         option = test_option)
### FD
testResultList = tc.testWith(testdata = df.DATA_NAME.__getitem__(name="FCC"),
                        service_provider = sf.PROVIDER.__getitem__(name="Kakao"),
                        service_type = SERVICE_TYPE.__getitem__(name="FD"),
                        option = test_option)

print("소요시간 : {}".format(time.time()-cur_time))

print("샘플수 : {}, 평균_정확도 : {}".format(testResultList[0], testResultList[1]))

