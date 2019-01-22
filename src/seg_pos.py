from src.boson import Boson
from os import path
import numpy as np
dir='/home/lnn/Documents/OpenNRE-Ina/OpenNRE-PyTorch/mnre_data'


import json
def pos_mnre(file_path,pos_path):
    ct=0
    bo=Boson()
    pos_res=[]
    with open(file_path) as f:
        bag=[]
        for line in f:
            sentence = line.strip('\n').strip('###END###').strip().split('\t')[5]
            bag.append(''.join(sentence.split()))
            ct+=1
            if len(bag)==100:
                print(ct)
                pos_res.extend(bo.seg(bag))
                bag=[]
                # break
        pos_res.extend(bo.seg(bag))
    json.dump({'mnre_data':pos_res},open(pos_path,mode='w'),ensure_ascii=False)
import time
def stanford_pos_mnre(file_path,pos_path):
    from stanfordcorenlp.corenlp import StanfordCoreNLP
    nlp = StanfordCoreNLP(r'/home/lnn/Downloads/postag/stanford-corenlp-full-2016-10-31/', lang='zh')

    pos_res=[]
    flg=True
    with open(file_path) as f:
        for i,line in enumerate(f):
            while flg:
                sentence = line.strip('\n').strip('###END###').strip().split('\t')[5]
                try:
                    s=nlp.pos_tag(''.join(sentence.split()))
                    flg=False
                except:
                    print('connection error sleep 60s')
                    time.sleep(60)

            pos_res.append([(j,i) for i,j in s])
            if i%100==0:
                print(i)
                # break
    np.save(pos_path,pos_res)
    # s=np.load(pos_path)
    # print(s)
    # json.dump({'mnre_data':pos_res},open(pos_path,mode='w'),ensure_ascii=False)


# stanford_pos_mnre(path.join(dir, 'valid_zh.txt'), path.join(dir,'valid_zh', 'stanford_valid_zh.npy'))

# pos_mnre(path.join(dir, 'train_zh.txt'), path.join(dir,'train_zh', 'train_zh.json'))

# s=np.load(path.join(dir,'train_zh', 'stanford_train_zh.npy'))
# print(len(s))