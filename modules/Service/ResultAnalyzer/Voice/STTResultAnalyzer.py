from Struct.Result import TestResult
from modules.Service.ResultAnalyzer.BaseResultAnalyzer import BaseResultAnalyzer
import logging

import re
import copy


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
        """테스트 결과(result)에 대한 정확도 및 통계수치를 분석하고 그 결과를 반환
        """

        ### add sample_info
        samples = self.resultStack['samples']
        if result.id not in samples:
            samples[result.id] = {}

        acc, acc_expected, acc_actual = self._calculateWERAccuracyWithNomalize(expectedList=result.expected, actualList=result.actual)
        samples[result.id] = {
            'service': result.service,
            'expected': acc_expected,
            'actual': acc_actual,
            'metric': 'Character Error Rate',
            'accuracy': float(acc)
        }

        ### add static_info
        statistics = self.resultStack['statistics']
        statistics['numOfSamples'] += 1
        statistics['accuracy_sum'] += float(acc)


    def _calculateWERAccuracyWithNomalize(self, expectedList:list, actualList:list) -> list:
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

                err_ins, err_del, err_sub, correction = self._levenshteinDistanceList(exp_sub, act_sub)
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


    def _levenshteinDistanceList(self, cmp1, cmp2):
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