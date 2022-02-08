from enum import Enum
import modules.Analysis.AnalysisToolForSTT as ast

class AccuracyFilter(Enum):
    EXP_BASED = ast.calculateSTTAccuracy
    WER = ast.calculateWERAccuracy

### get all keys
# [k for k in AccuracyFilter.__dict__.keys() if not k.startswith('_')]