# JEMHopQA

#### New Update (March 12, 2024)
We have added evaluation scripts and a sample of synonym dictionary.

#### New Update (November 10, 2023)
We have released [corpus_ver1.1](corpus_ver1.1) (`corpus_ver1.1/train_ver1.1.json`, `corpus_ver1.1/dev_ver1.1.json`), which contains several fixes for questions, answers, and triples.

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


| Key              | Description                                                | Example                                                      |
| :--------------- | :--------------------------------------------------------- | :----------------------------------------------------------- |
| `qid`            | Question ID                                                | `"2138f0638f363e75593d09df560db76c"`                         |
| `type`           | Question type                                              | `"comparison"`                                               |
| `question`       | Question                                                   | `"『仮面ライダー電王』と『あまちゃん』、放送回数が多いのはどちらでしょう？"` |
| `answer`         | Answer                                                     | `"あまちゃん"`                                               |
| `derivations`    | derivation steps                                           | `[["仮面ライダー電王", "放送回数", ["49"]], ["あまちゃん", "放送回数", ["156"]]]` |
| `page_ids`       | Page IDs of two Wikipedia articles                         | ` ["1398776","2588518"]`                                     |
| `time_dependent` | Flags questions for which answers may change in the future | `false`                                                      |

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
  "e": [0.8243644596919709, 0.8341406821599607, 0.8241752304610381],
  "r": [0.7168995180557596, 0.7183956173976581, 0.7094029197329732],
  "er": [0.7685931868076684, 0.7757018447656213, 0.7666854346880572]
}
```


## License and Acknowledgements

- This dataset is copyrighted by the [RIKEN](https://www.riken.jp/en/about/) and is licensed for use and redistribution under the terms of the [Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/legalcode.txt). 

  ![https://creativecommons.org/licenses/by-sa/4.0/legalcode](https://i.imgur.com/7HLJWMM.png)

- We would appreciate it if you could refer to the following references when presenting your research results using this dataset.

  - Ai Ishii, Naoya Inoue, Hisami Suzuki and Satoshi Sekine. "JEMHopQA: Improved Japanese Multi-Hop QA Dataset". Proceedings of the 30th Annual Conference of the Association for Natural Language Processing (NLP2024)
  - [石井愛, 井之上直也, 鈴木久美, 関根聡. JEMHopQA: 日本語マルチホップ QA データセットの改良. 言語処理学会第30回年次大会論文集, March 2024. (in japanese)](https://www.anlp.jp/proceedings/annual_meeting/2024/pdf_dir/P3-18.pdf) 

- This work was supported by the  JSPS Grants-in-Aid for Scientific Research JP20269633 and 19K20332. 

