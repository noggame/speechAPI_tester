import re
# import modules.Analysis.AnalysisToolForSTT as ast
from modules.AccuracyFilter import AccuracyFilter as AF

s = ['가와! 나#와 다', '안녕하세요']
cmp = ['가나다', '가와 나와 다']

print(AF.EXP_BASED(expectedList = s, actualList = cmp))
