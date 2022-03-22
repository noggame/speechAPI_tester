import os

### Indexing
targetDirPath = '/mnt/d/Workspace/python/speechAPI_tester/sample/shinhan/rename'
for root, dirs, files in os.walk(targetDirPath):
    # Converting
    for file in files:
        if file.endswith('.wav'):
            target = f"{root}/{file}"
            dest = f"{root}/{file[:2]}.wav"
            os.rename(target, dest)