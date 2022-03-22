import modules.SoundConverter as sc

### up-sampling
targetDirPath = '/mnt/d/Workspace/python/speechAPI_tester/sample/shinhan/split/1_20220111_101404438_2011.raw_Callee'
# targetDirPath = '/mnt/d/Workspace/python/speechAPI_tester/sample/shinhan/test'
sc.makeResamplingData(targetDirPath, 8000, 16000)