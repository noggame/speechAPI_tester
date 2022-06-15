from Struct.Result import TestResult
from modules.Service.Analyzer.BaseResultAnalyzer import BaseResultAnalyzer
# from Struct.Result.BaseResultRepository import STTResultRepository
# from modules.Service.Type import ACCURACY_STT
import json
import logging


class STTResultAnalyzer(BaseResultAnalyzer):
    def __init__(self) -> None:
        super().__init__()
        self.resultStack = {
            'statistics' : {
                'numOfSamples' : 0,
                'accuracy_sum' : 0
            },
            'samples' : {}
        }

    def analysisResultStack(self, resultList: list):
        for result in resultList:
            self._addResultToStack(result=result)

        samples = self.resultStack['statistics']['numOfSamples']
        accuracy_avg = float(self.resultStack['statistics']['accuracy_sum']/samples)

        return samples, accuracy_avg

    def _addResultToStack(self, result:TestResult):
        """ TestResult를 입력받아 분석하고, 분석 결과를 STT Analysis Reopistory에 저장
        """

        ### add sample_info
        samples = self.resultStack.get('samples')
        if result.id not in samples:
            samples[result.id] = {}

        acc, acc_expected, acc_actual = calculateWERAccuracyWithNomalize(expectedList=result.expected, actualList=result.actual)
        samples[result.id] = {
            'service': result.service,
            'expected': acc_expected,
            'actual': acc_actual,
            'metric': 'Character Error Rate',
            'accuracy': float(acc)
        }

        ### add static_info
        statistics = self.resultStack.get('statistics')
        statistics['numOfSamples'] += 1
        statistics['accuracy_sum'] += float(acc)


    # def startAnalysis(self, accuracyFilter:list=[], categoryFilter:list=[], sttResultData:list=None):
    #     _analysisRepo = STTResultRepository()

    #     ### Stack result on AnalysisRepository
    #     for eachTestResult in sttResultData:
    #         _analysisRepo.addAnalysisData(testResult = eachTestResult, accuracyFilter = accuracyFilter, categoryFilter = categoryFilter)


    #     return self._getStatics(analysisRepo=_analysisRepo)            


    # def _getStatics(self, analysisRepo:STTResultRepository):

    #     _ar:dict = json.loads(str(analysisRepo).replace("\'", "\""))

    #     staticRepo = {'total': 0}
    #     # staticRepo = {
    #     #    "total":35000,
    #     #    "EXP_BASED":{
    #     #       "KT_STT":{
    #     #          "NC":{
    #     #             "sample":15274,
    #     #             "acc_sum":1188084.430000014
    #     #          },
    #     #          "NA":{
    #     #             "sample":4855,
    #     #             "acc_sum":291369.5600000018
    #     #          }, ...
    #     #       },
    #     #       "Kakao_STT":{...}
    #     #    },
    #     #    "WER":{
    #     #       "KT_STT":{...},
    #     #       "Kakao_STT":{...}
    #     #    }
    #     # }

    #     # Statics
    #     for sample in _ar.values():
    #         staticRepo['total'] += 1
            
    #         for eachStatic in sample['statics']:
    #             service = eachStatic['service']
    #             categories = eachStatic['categories']
    #             acc_name = eachStatic['accuracy']['name']
    #             acc_rate = eachStatic['accuracy']['value']

    #             # create AccuracyType (ex_ [EXP_BASED, WER, ...])
    #             if acc_name not in staticRepo:
    #                 staticRepo[acc_name] = {}
                
    #             # create Service (ex_ KT, KAKAO)
    #             if service not in staticRepo[acc_name]:
    #                 staticRepo[acc_name][service] = {}
                
    #             service_in_repo:dict = staticRepo[acc_name][service]
    #             for ct in categories:
                    
    #                 # create Category (ex_ ['NA', 'NC', '예약', ...])
    #                 if ct not in service_in_repo:
    #                     service_in_repo[ct] = {}
    #                     service_in_repo[ct]['sample'] = 0
    #                     service_in_repo[ct]['acc_sum'] = 0

    #                 service_in_repo[ct]['sample'] += 1
    #                 service_in_repo[ct]['acc_sum'] += acc_rate

            
    #     ### Record
    #     # if record:
    #     #     file_record = open(record, 'w')
    #     #     file_record.write(str(_analysisRepo))
    #     #     file_record.close()

    #     # print Statics
    #     return self._parseStaticRepo(staticRepository = staticRepo)


    # def _parseStaticRepo(self, staticRepository:dict):
    #     result = ''

    #     for sKey, sValue in staticRepository.items():
    #         if sKey == 'total':
    #             result += '========================\n'
    #             result += 'total sample = {}\n'.format(sValue)
    #             result += '========================\n'
    #         else:
    #             result += '{} 정확도 측정 결과\n'.format(sKey)
    #             for serviceType, categoryInfo in sValue.items():               # Compare Method
    #                 result += '{0:<15}  '.format(serviceType)

    #                 s_sum = 0
    #                 s_sample = 0

    #                 for categoryType, staticInfo in categoryInfo.items():     # Service
    #                     result += '{} : {} % ({})'.format(categoryType, str(round(staticInfo['acc_sum']/staticInfo['sample'], 2)).ljust(5), staticInfo['sample'])
    #                     result += '{0:<4}'.format(' ')

    #                     # Not Applicable 제외한 전체 평균
    #                     if categoryType != 'NA':
    #                         s_sum += staticInfo['acc_sum']
    #                         s_sample += staticInfo['sample']

    #                 result += '전체평균 : {} %'.format(str(round(s_sum/s_sample, 2)).ljust(5))
    #                 result += '\n'

    #             result += '------------------------\n'

    #     return result
    #     # print(staticRepository)




















import re
import copy

def calculateWERAccuracyWithNomalize(expectedList:list, actualList:list) -> list:
    final_wer = 0
    hm_expected = ''    # highest matching
    hm_actual = ''

    for exp in expectedList:
        for act in actualList:
            if act == '':   # except empty result
                continue

            # except special char. and whitespace
            exp_sub = re.sub('[!@#$%^&*\(\).? \t]*', '', exp)
            act_sub = re.sub('[!@#$%^&*\(\).? \t]*', '', act)

            err_ins, err_del, err_sub, correction = levenshteinDistanceList(exp_sub, act_sub)
            # print(f'insertion    = {err_ins}')
            # print(f'deletion     = {err_del}')
            # print(f'substitution = {err_sub}')
            # print(f'correction   = {correction}')

            sum_ids = sum([err_ins, err_del, err_sub])
            sum_sdc = sum([err_sub, err_del, correction])
            cur_wer = (1-sum_ids/sum_sdc)*100
            
            # print("Accuracy = {}".format(cur_wer))
            # print("Correct = {}".format((1-(err_del+err_sub)/sum_sdc)*100))
            # print("[cor:{}, ins:{}, del:{}, sub:{}]\n".format(correction, err_ins, err_del, err_sub))

            if err_ins > 0 and cur_wer <= 0:     # nomalize
                cur_wer = (1-sum_ids/(sum_ids+correction))*100

            if cur_wer >= final_wer:
                final_wer = cur_wer
                hm_expected = exp
                hm_actual = act

    return [final_wer, hm_expected, hm_actual]


def levenshteinDistanceList(cmp1, cmp2):
    cmpAry = []
    correction = 0

    # init.
    for i in range(len(cmp1)+1):
        cmpAry.append([])
        for j in range(len(cmp2)+1):
            cmpAry[i].append([0, 0, 0])  # [Insertion, Deletion, Substituion, isCorrect]

            if i == 0:
                cmpAry[0][j] = [int(j), 0, 0]
            elif j == 0:
                cmpAry[i][0] = [0, int(i), 0]

    # calculation
    for i in range(1, len(cmp1)+1):
        for j in range(1, len(cmp2)+1):
            if cmp1[i-1] == cmp2[j-1]:
                cmpAry[i][j] = copy.deepcopy(cmpAry[i-1][j-1])

            else:
                insertion = sum(cmpAry[i][j-1][:]) + 1
                deletion = sum(cmpAry[i-1][j][:]) + 1
                substitution = sum(cmpAry[i-1][j-1][:]) + 1
                minValue = min(insertion, deletion, substitution)

                if minValue == insertion:
                    cmpAry[i][j] = [int(cmpAry[i][j-1][0])+1, int(cmpAry[i][j-1][1]), int(cmpAry[i][j-1][2])]
                elif minValue == deletion:
                    cmpAry[i][j] = [int(cmpAry[i-1][j][0]), int(cmpAry[i-1][j][1])+1, int(cmpAry[i-1][j][2])]
                elif minValue == substitution:
                    cmpAry[i][j] = [int(cmpAry[i-1][j-1][0]), int(cmpAry[i-1][j-1][1]), int(cmpAry[i-1][j-1][2])+1]
        
        # print("{} / {}".format(i, len(cmp1)))

    # print(*cmpAry, sep='\n')
    err_ins = cmpAry[len(cmp1)][len(cmp2)][0]
    err_del = cmpAry[len(cmp1)][len(cmp2)][1]
    err_sub = cmpAry[len(cmp1)][len(cmp2)][2]
    correction = len(cmp1) - err_del - err_sub

    return err_ins, err_del, err_sub, correction