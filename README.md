# updated by Ina Liu

* 数据处理
  * ctb文件转化成模型所需数据格式：cfg_data.py
  * 对新文本按照stanford和boson生成分词、词性标注文本：seg_pos.py boson.py
  * 中间结果lstm_out 输出：parser_lstm.py
  * 完整句法树输出：cp_out.py
  * 检查测试样本是否与训练样本有重复：check_test_data.py
  
* parser改动
  * 解析得到中间结果：parser.py
  
* 生成结果展示-test:evalb-result 
  * gold.txt    : 测试集实际句法结果
  * predict.txt : 预测结果
  * output.txt  : precision-recall-f1 计算详细结果
  
(S (IP (NP-SBJ (NP-PN (NR 中国)) (NP (NN 政府))) (VP (VP (VV 鼓励) (NP-OBJ (-NONE- *RNR*-1)) (QP-EXT (-NONE- *RNR*-2))) (CC 和) (VP (VV 支持) (NP-OBJ-1 (NP-PN (NR 中国)) (NP (NN 企业界))) (IP-2 (NP-SBJ (-NONE- *PRO*)) (VP (PP-LOC (P 在) (LCP (NP (CP-APP (IP (NP-SBJ (-NONE- *PRO*)) (VP (VCD (VA 平等) (VV 互利)))) (DEC 的)) (NP (NN 基础))) (LC 上))) (VP (VV 参与) (NP-OBJ (DNP (NP-PN (NR 吉尔吉斯)) (DEG 的)) (NP (NN 经济) (NN 建设)))))))) (PU 。) (PU ”)))
(S (IP (NP-SBJ (NP-PN (NR 中国)) (NP (NN 政府))) (VP (VP (VV 鼓励) (NP-OBJ (-NONE- *RNR*-1)) (QP-EXT (-NONE- *RNR*-2))) (CC 和) (VP (VV 支持) (NP-OBJ-1 (NP-PN (NR 中国)) (NP (NN 企业界))) (IP-2 (NP-SBJ (-NONE- *PRO*)) (VP (PP-LOC (P 在) (LCP (NP (CP-APP (IP (NP-SBJ (-NONE- *PRO*)) (VP (VCD (VA 平等) (VV 互利)))) (DEC 的)) (NP (NN 基础))) (LC 上))) (VP (VV 参与) (NP-OBJ (DNP (NP-PN (NR 吉尔吉斯)) (DEG 的)) (NP (NN 经济) (NN 建设)))))))) (PU 。) (PU ”)))

(S (IP (NP-SBJ (PU “) (NP (NP (NP-PN (NR 中) (NR 美)) (NP (NN 合作))) (NP     (ADJP (JJ 高)) (NP (NN 科技))) (NP (NN 项目))) (NP (NN 签字) (NN 仪式)) (PU ”)) (VP (NP-TMP (NT 今天)) (PP-LOC (P 在) (NP-PN (NR 上海))) (VP (VV 举行))) (PU 。)))
(S (IP (NP-SBJ (PU “) (NP     (NP-PN (NR 中) (NR 美)) (NP (NN 合作))) (NP (NP (ADJP (JJ 高)) (NP (NN 科技))) (NP (NN 项目))) (NP (NN 签字) (NN 仪式)) (PU ”)) (VP (NP-TMP (NT 今天)) (PP-LOC (P 在) (NP-PN (NR 上海))) (VP (VV 举行))) (PU 。)))

# Minimal Span-Based Neural Constituency Parser

This is a reference Python implementation of the top-down and chart-based constituency parsers described in [A Minimal Span-Based Neural Constituency Parser](https://arxiv.org/abs/1705.03919) from ACL 2017.

The top-down parser is implemented as described in the paper.

The chart parser includes the simplifications outlined in the ACL 2017 oral presentation, namely:

  * Removing the unlabeled span-scoring terms from the model.
  * Fixing the score of the empty label at 0.

These changes improve speed and reduce memory usage without affecting final performance. Moreover, they result in the score of a tree decomposing directly into a sum of labeled span scores, eliminating score differences that arise due to different choices of binarization.

## Requirements and Setup

* Python 3.5 or higher.
* [DyNet](https://github.com/clab/dynet). We recommend installing DyNet from source with MKL support for significantly faster run time.
* [EVALB](http://nlp.cs.nyu.edu/evalb/). Before starting, run `make` inside the `EVALB/` directory to compile an `evalb` executable. This will be called from Python for evaluation.
* Pre-trained models. Before starting, run `unzip zipped/top-down-model_dev=92.34.zip` and `unzip zipped/chart-model_dev=92.24.zip` in the `models/` directory to extract the pre-trained models.

## Training

A new model can be trained using the command `python3 src/main.py train ...` with the following arguments:

Argument | Description | Default
--- | --- | ---
`--numpy-seed` | NumPy random seed | Random
`--parser-type` | `top-down` or `chart` | N/A
`--tag-embedding-dim` | Tag embedding dimension | 50
`--word-embedding-dim` | Word embedding dimension | 100
`--lstm-layers` | Number of bidirectional LSTM layers | 2
`--lstm-dim` | Hidden dimension of each LSTM within each layer | 250
`--label-hidden-dim` | Hidden dimension of label-scoring feedforward network | 250
`--split-hidden-dim`* | Hidden dimension of split-scoring feedforward network | 250
`--dropout` | Dropout rate for LSTMs | 0.4
`--explore`* | Train with exploration using a dynamic oracle | Train using a static oracle
`--model-path-base` | Path base to use for saving models | N/A
`--evalb-dir` |  Path to EVALB directory | `EVALB/`
`--train-path` | Path to training trees | `data/02-21.10way.clean`
`--dev-path` | Path to development trees | `data/22.auto.clean`
`--batch-size` | Number of examples per training update | 10
`--epochs` | Number of training epochs | No limit
`--checks-per-epoch` | Number of development evaluations per epoch | 4
`--print-vocabs` | Print the vocabularies before training | Do not print the vocabularies

\*These arguments only apply to the top-down parser.

Any of the DyNet command line options can also be specified.

The training and development trees are assumed to have predicted part-of-speech tags.

For each development evaluation, the F-score on the development set is computed and compared to the previous best. If the current model is better, the previous model will be deleted and the current model will be saved. The new filename will be derived from the provided model path base and the development F-score.

As an example, to train a top-down parser with exploration using the default hyperparameters, you can use the command:

```
python3 src/main.py train --parser-type top-down --explore --model-path-base models/top-down-model
```

Alternatively, to train a chart parser using the default hyperparameters, you can use the command:

```
python3 src/main.py train --parser-type chart --model-path-base models/chart-model
```

Compressed pre-trained models with these settings are provided in the `models/zipped/` directory. See the section above for extraction instructions.

## Evaluation

A saved model can be evaluated on a test corpus using the command `python3 src/main.py test ...` with the following arguments:

Argument | Description | Default
--- | --- | ---
`--model-path-base` | Path base of saved model | N/A
`--evalb-dir` |  Path to EVALB directory | `EVALB/`
`--test-path` | Path to test trees | `data/23.auto.clean`

As above, any of the DyNet command line options can also be specified.

The test trees are assumed to have predicted part-of-speech tags.

As an example, after extracting the pre-trained top-down model, you can evaluate it on the test set using the following command:

```
python3 src/main.py test --model-path-base models/top-down-model_dev=92.34
```

The pre-trained top-down model obtains F-scores of 92.34 on the development set and 91.80 on the test set. The pre-trained chart model obtains F-scores of 92.24 on the development set and 91.86 on the test set.

## Parsing New Sentences

The `parse` method of a parser can be used to parse new sentences. In particular, `parser.parse(sentence)` will return a tuple containing the predicted tree and a DyNet expression for the score of the tree under the model. The input sentence should be pre-tagged and represented as a list of (tag, word) pairs.

See the `run_test` function in `src/main.py` for an example of how a parser can be loaded from disk and used to parse sentences.

## Citation

If you use this software for research, please cite our paper as follows:

```
@InProceedings{Stern2017Minimal,
  author    = {Stern, Mitchell and Andreas, Jacob and Klein, Dan},
  title     = {A Minimal Span-Based Neural Constituency Parser},
  booktitle = {Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)},
  month     = {July},
  year      = {2017},
  address   = {Vancouver, Canada},
  publisher = {Association for Computational Linguistics},
  pages     = {818--827},
  url       = {http://aclweb.org/anthology/P17-1076}
}
```
