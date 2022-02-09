from enum import Enum
import modules.Accuracy.STTAccuracyTool as sat

class AccuracyFilter(Enum):
    EXP_BASED = sat.calculateSTTAccuracy
    WER = sat.calculateWERAccuracy

### get all keys
# [k for k in AccuracyFilter.__dict__.keys() if not k.startswith('_')]