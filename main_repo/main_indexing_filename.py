import os

### Indexing
targetDirPath = "/Users/songdonghun/dataset/STT/shinhan/0422_yes/1_20220111_164634311_2002.raw_Callee"
for root, dirs, files in os.walk(targetDirPath):
    # Converting
    for file in files:
        if file.endswith('.wav'):
            idx = file.split("-")[0]
            
            target = f"{root}/{file}"
            dest = f"{root}/{idx}.wav"
            os.rename(target, dest)