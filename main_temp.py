import modules.SoundConverter as sc
import os


### up-sampling
# # targetDirPath = '/mnt/d/Workspace/python/speechAPI_tester/sample/shinhan/1_20220111_101404438_2011.raw_Callee'
# targetDirPath = '/mnt/d/Workspace/python/speechAPI_tester/sample/shinhan/test'
# sc.makeResamplingData(targetDirPath, 8000, 16000)



### Indexing
targetDirPath = '/mnt/d/Workspace/python/speechAPI_tester/sample/shinhan/1_20220111_101404438_2011.raw_Callee'
for root, dirs, files in os.walk(targetDirPath):
    # Converting
    for file in files:
        if file.endswith('.wav'):
            target = f"{root}/{file}"
            dest = f"{root}/{file[:2]}.wav"
            os.rename(target, dest)
