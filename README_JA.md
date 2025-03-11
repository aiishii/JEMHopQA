# JEMHopQA

#### New Update (March 11, 2025)

段階的RAGシステムの実装リポジトリ [multihop_staged_rag](https://github.com/aiishii/multihop_staged_rag) を公開しました。このリポジトリでは、論文「構造化知識 RAG・文書ベース RAG を段階的に利用したマルチホップ QA に対する LLM の精度向上」で提案した手法の実装を提供しています。（⚠️ 2025年4月までに完全版を公開予定）

#### New Update (March 12, 2024)

評価用スクリプトと、スクリプト内で使用する類義語辞書のサンプルを追加しました。

#### New Update (November 10, 2023)

[corpus_ver1.1](corpus_ver1.1) (`corpus_ver1.1/train_ver1.1.json`, `corpus/dev_ver1.1.json`)をリリースしました。 このリリースには、質問、回答、トリプルのいくつかの修正が含まれています。

## はじめに

JEMHopQA (Japanese Explainable Multi-hop Question Answering)は、回答導出ステップの情報付きの日本語の根拠情報付きマルチホップQAデータセットです。質問 (Question)を入力として、回答 (Answer)と導出 (Derivation)を生成するタスクです。導出は導出ステップの集合で、半構造化されたエンティティ間の関係表現です。問題は、Wikipediaの２つの記事の情報をリンクさせて答える構成問題 (compositional)と2つの記事の情報を比較して答える比較問題 (comparison)が含まれています。

本レポジトリは以下のデータセットおよびスクリプトを提供します。

- JEMHopQA Corpus (`corpus/train.json`, `corpus/dev.json`)
- 評価スクリプト (`evaluate.py`)
- クラウドソーシングインターフェース (TBA)

また、本データセットは以下のWikipediaのバージョンに対応しています。[森羅プロジェクト](http://shinra-project.info/)のページからダウンロードしてご使用ください。

* [Wikipedia2021 (HTML)](https://storage.googleapis.com/shinra_data/wikipedia/wikipedia-ja-20210820-html-v2.zip)
* [Wikipedia2021 (JSON形式、CirrusSearchDump)](https://storage.googleapis.com/shinra_data/wikipedia/wikipedia-ja-20210823-json.gz)



## データ仕様

質問、回答、導出のセットは以下のJSONフォーマットで提供します。

| キー             | 説明                                     | 例                                                           |
| :--------------- | :--------------------------------------- | :----------------------------------------------------------- |
| `qid`            | 問題ID                                   | `"2138f0638f363e75593d09df560db76c"`                         |
| `type`           | 問題種別                                 | `"comparison"`                                               |
| `question`       | 問題文                                   | `"『仮面ライダー電王』と『あまちゃん』、放送回数が多いのはどちらでしょう？"` |
| `answer`         | 回答                                     | `"あまちゃん"`                                               |
| `derivations`    | 導出ステップ                             | `[["仮面ライダー電王", "放送回数", ["49"]], ["あまちゃん", "放送回数", ["156"]]]` |
| `page_ids`       | 2つのWikipediaページのページID           | ` ["1398776","2588518"]`                                     |
| `time_dependent` | 将来答えが変わる可能性のある問題のフラグ | `false`                                                      |



### 実際のデータ例

以下に質問、回答、導出のセットのデータ例を示します．

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



## データの統計量

|                    | 問題数（計） | 構成問題 | 比較問題 |
| :----------------- | -----------: | -------: | -------: |
| 訓練データ (train) |         1059 |      392 |      667 |
| 開発用データ (dev) |          120 |       47 |       73 |
| 合計               |         1179 |      439 |      740 |



# 評価用スクリプト

評価用スクリプト(`evaluate.py`) は [R4C](https://github.com/naoya-i/r4c/blob/master/src/r4c_evaluate.py) の評価スクリプトに日本語の処理を追加したものです。

## 使用ライブラリ

以下のPythonパッケージをインストールしてください。

- `pulp`
- `Levenshtein`
- `tqdm`
- `chikkarpy`
- `sudachipy`

## Predictionファイルフォーマット

Predictionファイルのフォーマットは以下の例のとおりです。

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

## 実行方法

回答と導出の予測結果 (`/path/to/your_prediction.json`)を評価するには以下のコマンドを実行してください。



`python evaluate.py --pred /path/to/your_prediction.json --label corpus_ver1.1/dev_ver1.1.json`



TSV形式の予測結果 (`/path/to/your_gpt_prediction.tsv` カラム：qid, predicted_answer, predicted_derivations)をJSONに変換するスクリプトを以下のように利用できます。



`python3 tsv_to_pred_json.py -tsv /path/to/your_gpt_prediction.tsv -out /path/to/your_prediction.json`

## 出力フォーマット

評価スクリプトの出力は以下のエンティティからなるJSON形式です。

- `"a"`:回答の*em*(exact match), *score*(similarity match) 
- `"e"`:導出の*entity-level*のprecision, recall, f1
- `"r"`: 導出の*relation-level* のprecision, recall, f1
- `"er"`:  導出の*full* precision, recall, f1

出力の例は以下の通りです。

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

## 関連リポジトリ

JEMHopQAデータセットを利用した実装として、以下のリポジトリも公開しています：

- [multihop_staged_rag](https://github.com/aiishii/multihop_staged_rag) - 構造化知識 RAG・文書ベース RAG を段階的に利用したマルチホップ QA システムの実装（⚠️ 2025年4月までに完全版を公開予定）


## ライセンス・謝辞

- 本データセットの著作権は[理化学研究所](https://www.riken.jp/)に帰属し、 [クリエイティブ・コモンズ 表示 - 継承 4.0 国際 ライセンス (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/legalcode.txt)*の条件のもとに、利用・再配布が許諾されます。*

  ![https://creativecommons.org/licenses/by-sa/4.0/legalcode](https://i.imgur.com/7HLJWMM.png)

- 本データセットを利用した研究成果を発表される際は、以下の文献を参照いただけますと幸いです。

  - Ai Ishii, Naoya Inoue, Hisami Suzuki, and Satoshi Sekine. 2024. [JEMHopQA: Dataset for Japanese Explainable Multi-Hop Question Answering](https://aclanthology.org/2024.lrec-main.831/). In Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING 2024), pages 9515–9525, Torino, Italia. ELRA and ICCL.

- 本データセット構築の一部はJSPS 科研費 JP20269633 および 19K20332 の助成を受けたものです。記して感謝いたします。

