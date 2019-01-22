from os import path
from nltk.corpus.reader.util import find_corpus_fileids
from nltk.data import FileSystemPathPointer
home_dir=path.join(path.dirname(__file__),'./')
import re
# ctb_dir = '/home/lnn/Downloads/ctb_test'
ctb_dir = '/home/lnn/Downloads/ctb_paper/origin/out_paper'
# ctb_dir = '/home/lnn/Documents/ability/cranfield_testdata/upenn_transfer/normal_ctb_test'
# ctb_dir = '/home/nana/Documents/pycharmforlinux/upenn_transfer/normal_ctb_test_v1'

ctb_path=path.join(ctb_dir,'ctb.secondtest.clean')
counts=0
fc=open(ctb_path,mode='w',encoding='utf-8')
# reg = 'chtb_3095.bn'
reg = '(.*nw)*(.*bc)*(.*mz)*(.*bn)*(.*wb)*'
# reg = '(.*nw)*(.*mz)*'
ctb_dir = FileSystemPathPointer(ctb_dir)
fileids = find_corpus_fileids(root=ctb_dir, regexp=reg)

OTHER=['］','［','）','（','＜','／','＞']

def strQ2B(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 12288:                              #全角空格直接转换
            inside_code = 32
        elif (inside_code >= 65281 and inside_code <= 65374): #全角字符（除空格）根据关系转化
            inside_code -= 65248

        rstring += chr(inside_code)
    return rstring

for fileid in fileids:
    with open(path.join(ctb_dir,fileid)) as f:
        fs=[]
        sline=''
        for line in f.readlines():
            i=0
            while i<len(OTHER):
                if line.find(OTHER[i])>=0:
                    break
                i+=1
            if i==len(OTHER):
                line = strQ2B(line)
            # else:
            #     print(line)

            # if line.find('NR')>=0:
            #     print(line)
            #     print(fileid)
            if re.search('<\/.*>|<.*>',line)!=None :
                continue
            if re.match('\((\s)*\(',line)!=None:
                if sline.replace('\n','').replace('\t','').strip()!='':
                    fs.append(sline)
                    sline=''
            sline += line
        if sline.replace('\n','').replace('\t','').strip()!='':
            fs.append(sline)
        for s in fs:
            s=s.replace('\n','').replace('\t','').strip()
            # a=s[-1]
            # if s[1:-1]=='':
            #     continue
            # if s.find('(VP (ADVP (d 特别)) (VP (vyou 有) (NP-OBJ (v 批准)))))))        (f 之外)))')>=0:
            #     print(fileid)
            s='(TOP (S{}))'.format(s[1:-1])
            counts+=1
            fc.write(s+'\n')
    if counts>=5000:
        break



print(counts)#51447
fc.close()


