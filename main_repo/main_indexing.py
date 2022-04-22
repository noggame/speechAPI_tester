import os

baseDir = "/Users/songdonghun/dataset/STT/shinhan/0422_yes/1_20220111_101404438_2011.raw_Callee"
# baseDir = "/Users/songdonghun/dataset/STT/shinhan/0422_yes/1_20220111_154036778_2010.raw_Callee"
# baseDir = "/Users/songdonghun/dataset/STT/shinhan/0422_yes/1_20220111_160954259_2108.raw_Callee"
# baseDir = "/Users/songdonghun/dataset/STT/shinhan/0422_yes/1_20220111_164634311_2002.raw_Callee"
f_exp = open(f'{baseDir}/expect.txt', 'r')
f_new = open(f'{baseDir}/expect_rewirtten.txt', 'w')

index = 1
for line in f_exp.readlines():
    f_new.write(str(index).rjust(3, '0') + "\t" + line)
    index += 1

f_exp.close()
f_new.close()
