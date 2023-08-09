# JEMHopQA

## はじめに

JEMHopQA (Japanese Explainable Multi-hop Question Answering)は、回答導出ステップの情報付きの日本語の根拠情報付きマルチホップQAデータセットです。質問 (Question)を入力として、回答 (Answer)と導出 (Derivation)を生成するタスクです。導出は導出ステップの集合で、半構造化されたエンティティ間の関係表現です。問題は、Wikipediaの２つの記事の情報をリンクさせて答える構成問題 (compositional)と2つの記事の情報を比較して答える比較問題 (comparison)が含まれています。

本レポジトリは以下のデータセットおよびスクリプトを提供します。

- JEMHopQA Corpus (`corpus/train.json`, `corpus/dev.json`)
- 評価スクリプト (TBA)
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



## ライセンス・謝辞

- 本データセットの著作権は[理化学研究所](https://www.riken.jp/)に帰属し、 [クリエイティブ・コモンズ 表示 - 継承 4.0 国際 ライセンス (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/legalcode.txt)*の条件のもとに、利用・再配布が許諾されます。*

  ![https://creativecommons.org/licenses/by-sa/4.0/legalcode](https://i.imgur.com/7HLJWMM.png)

- 本データセットを利用した研究成果を発表される際は、以下の文献を参照いただけますと幸いです。

  - 石井愛, 井之上直也, 関根聡. 根拠を説明可能な質問応答システムのための日本語マルチホップQAデータセット構築. 言語処理学会第29回年次大会論文集, 4 pages, March 2023.

  - [https://www.anlp.jp/proceedings/annual_meeting/2023/pdf_dir/Q8-14.pdf](https://www.anlp.jp/proceedings/annual_meeting/2023/pdf_dir/Q8-14.pdf)

- Special thanks: 鈴木久美先生

- 本データセット構築の一部はJSPS 科研費 JP20269633 および 19K20332 の助成を受けたものです。記して感謝いたします。

