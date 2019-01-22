
dir='/home/lnn/Downloads/minimal-span-parser-master/data/ctb_origin'

data={}

# with open()

import os

# print(os.listdir(dir))




def read(path,ct,write=False):
    if write:
        new=[]
    with open(path,errors='ignore') as f:
        for line in f:
            if line in data:
                print(path,data[line])
                ct=ct+1
                continue
            else:
                if write:
                    new.append(line)
                data[line]=path
    if write:
        print('new data ct:{}'.format(len(new)))
        with open(path,mode='w') as f:
            for i in new:
                f.write(i)
    return ct

ct=0
# for fname in os.listdir(dir):
#     ct=read(os.path.join(dir,fname),ct)
    # break
#
# print(ct,len(data))
ct=read(os.path.join(dir,'ctb.train.clean'),ct)
ct=read(os.path.join(dir,'ctb.dev.clean'),ct)
ct=0
print('======================================================')
ct=read(os.path.join(dir,'ctb.test.clean'),ct,write=True)
print(ct)
# print(ct,len(data))


