# JEMHopQA

#### New Update (March 11, 2025)

We have released [corpus_ver1.2](corpus_ver1.2) (`corpus_ver1.2/train_ver1.2.json`, `corpus_ver1.2/dev_ver1.2.json`), which contains several fixes for questions, answers, and triples.

#### New Update (March 11, 2025)

We have released the implementation repository [multihop_staged_rag](https://github.com/aiishii/multihop_staged_rag) for our staged RAG system. This repository provides the implementation of the approach proposed in our paper "Improving LLM Accuracy for Multi-hop QA through Staged Utilization of Structured Knowledge RAG and Document-based RAG." (⚠️ Full version to be released by April 2025)

## Introduction

JEMHopQA (Japanese Explainable Multi-hop Question Answering) is a Japanese multi-hop QA dataset that can evaluate internal reasoning. It is a task that takes a question as input and generates an answer and derivations. Derivations are a set of derivation steps and is a semi-structured representation of relationships between entities. This dataset contains both compositional (linking information from two Wikipedia articles) and comparison (comparing information from two Wikipedia articles) questions.

This repository contains the following datasets and script:

- JEMHopQA Corpus (`corpus/train.json`, `corpus/dev.json`)
- Evaluation script (`evaluate.py`)
- Crowdsourcing interface (TBA)

This dataset is compatible with the following Wikipedia versions. Please download and use it from the [SHINRA Project](http://shinra-project.info/) page.

* [Wikipedia2021 (HTML)](https://storage.googleapis.com/shinra_data/wikipedia/wikipedia-ja-20210820-html-v2.zip)
* [Wikipedia2021 (JSON, CirrusSearchDump)](https://storage.googleapis.com/shinra_data/wikipedia/wikipedia-ja-20210823-json.gz)

## Data format

The question, answer, and derivation sets are provided in the following JSON format.

| Key                | Description                                                | Example                                                                             |
| :----------------- | :--------------------------------------------------------- | :---------------------------------------------------------------------------------- |
| `qid`            | Question ID                                                | `"2138f0638f363e75593d09df560db76c"`                                              |
| `type`           | Question type                                              | `"comparison"`                                                                    |
| `question`       | Question                                                   | `"『仮面ライダー電王』と『あまちゃん』、放送回数が多いのはどちらでしょう？"`      |
| `answer`         | Answer                                                     | `"あまちゃん"`                                                                    |
| `derivations`    | derivation steps                                           | `[["仮面ライダー電王", "放送回数", ["49"]], ["あまちゃん", "放送回数", ["156"]]]` |
| `page_ids`       | Page IDs of two Wikipedia articles                         | ` ["1398776","2588518"]`                                                          |
| `time_dependent` | Flags questions for which answers may change in the future | `false`                                                                           |

### Example of data

Below is an example of data for a set of questions, answers, and derivations.

```
[
	{
		"qid": "45cad48d43f222048ea4a498fd29c4a1",
		"type": "comparison",
		"question": "『仮面ライダー電王』と『あまちゃん』、放送回数が多いのはどちらでしょう？",
		"answer": "あまちゃん",
		"derivations": [["仮面ライダー電王","放送回数",["49"]],["あまちゃん","放送回数",["156"]],
		"page_ids": ["1398776","2588518"],
		"time_dependent": false
	},
	{
		"qid": "50faa6719d85a03ae2d5b40d24c8987c",
		"type": "compositional",
		"question": "孝明天皇が生涯過ごした都に以前の都から遷都があった年は？",
		"answer": "794年",
		"derivations": [["孝明天皇","生涯を過ごした都",["平安京"]],["平安京","遷都された年",["794年"]]],
		"page_ids": ["266469","7171"],
		"time_dependent": false
	},
...
```

## Data Statistics

|           |  all | compositional | comparison |
| :-------- | ---: | ------------: | ---------: |
| train set | 1059 |           392 |        667 |
| dev set   |  120 |            47 |         73 |
| total     | 1179 |           439 |        740 |

# Evaluation script

Evaluation script (`evaluate.py`) is forked from [https://github.com/naoya-i/r4c/](https://github.com/naoya-i/r4c/blob/master/src/r4c_evaluate.py) and adds Japanese processing.

Additionally, an LLM-based evaluation script inspired by [CRAG (Contrastive Retrieval-Augmented Generation)](https://github.com/facebookresearch/CRAG) is available [here](https://github.com/aiishii/multihop_staged_rag/tree/main/src/evaluation) (⚠️ Full version to be released by April 2025).

## Dependency

Please install the following Python packages:

- `pulp`
- `Levenshtein`
- `tqdm`
- `chikkarpy`
- `sudachipy`

## Prediction file format

On top of `answer` key (answers) and `derivations` key for derivations. The value of `derivations` should be a dictionary, where the key is a `qid` and the value is a derivation.
An example is given below.

```
{
  "answer": {
    "2138f0638f363e75593d09df560db76c": "ファイナルファンタジーXIII",
    ...
  },
  "derivations": {
    "2138f0638f363e75593d09df560db76c": [
      [
        "ダンガンロンパ 希望の学園と絶望の高校生", 
        "発売日", 
        ["2010年11月25日"]
      ], 
      [
        "ファイナルファンタジーXIII", 
        "発売日", 
        ["2009年12月17日"]
      ]
    ],
    ...
  }
}
```

## How to run

To evaluate your prediction (say `/path/to/your_prediction.json`), run the following command:

`python evaluate.py --pred /path/to/your_prediction.json --label corpus_ver1.1/dev_ver1.1.json`

If you have output in TSV (`/path/to/your_gpt_prediction.tsv` has following columns: qid, predicted_answer, predicted_derivations), you can convert it to JSON with `tsv_to_pred_json.py` script.

`python3 tsv_to_pred_json.py -tsv /path/to/your_gpt_prediction.tsv -out /path/to/your_prediction.json`

## Output format

The script outputs a JSON dictionary consisting of three entries:

- `"a"`: answer's *em* (exact match) and *score* (similarity match)
- `"e"`: derivation's entity-level* precision, recall, and f1.
- `"r"`: derivation's *relation-level* precision, recall, and f1.
- `"er"`: derivation's *full* precision, recall, and f1.

An example is given below.

```
{
  "a": {
    "em": 0.6083333333333333, 
    "score": 0.6402777777777778
  }, 
  "e": {
    "prec": 0.6740724206349207, 
    "recall": 0.6534143518518519, 
    "f1": 0.6587781084656084
  }, 
  "r": {
    "prec": 0.7197156084656083, 
    "recall": 0.6965674603174603, 
    "f1": 0.7038822751322751
  }, 
  "er": {
    "prec": 0.6878979276895943, 
    "recall": 0.6664098324514991, 
    "f1": 0.6724239417989417
  }
}
```

## Related Repositories

We also provide the following repository that uses the JEMHopQA dataset:

- [multihop_staged_rag](https://github.com/aiishii/multihop_staged_rag) - Implementation of a multi-hop QA system that uses structured knowledge RAG and document-based RAG in a staged manner (⚠️ Full version to be released by April 2025)

## License and Acknowledgements

- This dataset is copyrighted by the [RIKEN](https://www.riken.jp/en/about/) and is licensed for use and redistribution under the terms of the [Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/legalcode.txt).

  ![https://creativecommons.org/licenses/by-sa/4.0/legalcode](https://i.imgur.com/7HLJWMM.png)
- We would appreciate it if you could refer to the following references when presenting your research results using this dataset.

  - Ai Ishii, Naoya Inoue, Hisami Suzuki, and Satoshi Sekine. 2024. [JEMHopQA: Dataset for Japanese Explainable Multi-Hop Question Answering](https://aclanthology.org/2024.lrec-main.831/). In Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING 2024), pages 9515–9525, Torino, Italia. ELRA and ICCL.
- This work was supported by the  JSPS Grants-in-Aid for Scientific Research JP20269633 and 19K20332.
