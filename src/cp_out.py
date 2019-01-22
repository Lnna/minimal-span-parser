
from os import path
import pickle as pc
import dynet as dy
import numpy as np
import json
dir='/home/lnn/Documents/OpenNRE-Ina/OpenNRE-PyTorch/mnre_data'

print("Loading model from {}...".format('/home/lnn/Downloads/minimal-span-parser-master/models/top-down-model_dev=87.21'))
model = dy.ParameterCollection()
[parser] = dy.load('/home/lnn/Downloads/minimal-span-parser-master/models/top-down-model_dev=87.21', model)

def cparse(pos_file, parse_file):
    if pos_file.find('.json')>=0:
        data=json.load(open(pos_file))['mnre_data']
    else:
        data=np.load(pos_file)


    f = open(parse_file, mode='a')
    for m,line in enumerate(data):
        # if m<=154000:
        #     continue
        line=[tuple(i) for i in line]
        dy.renew_cg()
        try:
            lo,_ = parser.parse(line)
            per=lo.convert().linearize()
        except ValueError as e:
            print(e)
            print(line)
            per=''
        if m%1000==0:
            print(m)
            # break
        f.write(per+'\n')


    f.close()

cparse(path.join(dir, 'test_zh', 'stanford_test_zh.json'), path.join(dir, 'test_zh', 'bigdata_stanford_test_out.txt'))
