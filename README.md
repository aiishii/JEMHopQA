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
