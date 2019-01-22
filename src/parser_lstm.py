from src.boson import Boson
from os import path
import pickle as pc
import dynet as dy
import numpy as np
import json
dir='/home/lnn/Documents/OpenNRE-Ina/OpenNRE-PyTorch/mnre_data'

print("Loading model from {}...".format('/home/lnn/Downloads/minimal-span-parser-master/models/top-down-model_dev=87.21'))
model = dy.ParameterCollection()
[parser] = dy.load('/home/lnn/Downloads/minimal-span-parser-master/models/top-down-model_dev=87.21', model)
dim=500


def lstm_parse(pos_file,lstm_file):
    if pos_file.find('.json')>=0:
        data=json.load(open(pos_file))['mnre_data']
        l=len(data)
    else:
        data=np.load(pos_file)
        l=len(data)


    if path.exists(lstm_file):
        lstm_outs=np.load(lstm_file)
    else:

        lstm_outs = np.zeros((l, 500), dtype=np.float)
    # ct=0
    # for i in lstm_outs:
    #     if not i.any():
    #         ct+=1
    # print(ct)
    # return ct

    for m,line in enumerate(data):
        # if m<=154000:
        #     continue
        line=[tuple(i) for i in line]
        dy.renew_cg()
        try:
            lo = parser.parts_parse(line)
            lstm_outs[m]=lo[-1].npvalue()
        except ValueError as e:
            print(e)
            print(line)
            lstm_outs[m]=np.random.standard_normal((500,))
        if m%100==0:
            print(m)
            # break

        if m%1000==0:
            np.save(lstm_file,lstm_outs)
    np.save(lstm_file, lstm_outs)


def load_parse_res(ppath):
    parser=pc.load(open(ppath,mode='rb'))
    print(len(parser))
    print(parser)


lstm_parse(path.join(dir,'test_zh','stanford_test_zh.json'),path.join(dir,'test_zh','big_stanford_test_lstm_out.npy'))

# pos_mnre(path.join(dir, 'train_zh.txt'), path.join(dir,'train_zh', 'train_zh.json'))