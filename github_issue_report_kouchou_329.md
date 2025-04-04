# GitHub Issue レポート: digitaldemocracy2030/kouchou-ai

期間: 2025-03-22 から 2025-03-29 まで

## 過去1週間に完了されたissue (25件)

### [[DOCUMENT] 環境変数を書き換えた場合は docker compose up --build を実行するようにREADMEに追記する](https://github.com/digitaldemocracy2030/kouchou-ai/issues/191)

**作成者:** nasuka  
**作成日:** 2025-03-28T06:16:48Z  
**内容:**

# 現在の問題点
* 環境変数を変更した場合はdocker imageをbuildしなおさないと動作しないケースがある
  * フロントでは、APIキーなどの一部の環境変数をimageのビルド時に埋め込んでいる
  * このため、フロント側はdocker compose upを実行すると初回に設定した環境変数のイメージのままコンテナが立て続けられてしまう（ビルド時に埋め込んでいる環境変数は、イメージをビルドし直さない限り.envを編集しても変更が反映されない）
    * これにより以下の様にapiとフロントのAPIキーが一致しないケースが発生してしまう

```
1: デプロイの作業をしてたディレクトリでそのまま新機能開発をしようとしてdocker-compose upしたら起動はしたけど管理画面がAPIサーバに繋がらなくてスピナーが回りっぱなし
2: 原因は401 unauthorized
3: docker-compose upすると、compose.yamlのclient-adminはAPIサーバに接続するためのAPIキーをargsでハードコードしているので管理画面には古いキーが環境変数として渡される、一方でserverの方はそれをしないで.envを渡しているのでこちらは新しいAPIキーが渡される、不一致なので繋がらない
```

# 提案内容
* 環境変数を書き換えた場合は `docker compose up --build` を実行するようにREADMEに追記する


**コメント:** なし

---

### [[FEATURE]スプレッドシートでデータを取得した後にレポートIDを変更して作成を実行するとコメントデータが二重に保管される](https://github.com/digitaldemocracy2030/kouchou-ai/issues/184)

**作成者:** nasuka  
**作成日:** 2025-03-26T06:42:10Z  
**内容:**

# 背景
* レポート作成画面において、スプレッドシートからデータを取得した後にレポートのIDを変更すると、コメントのデータが二重に保管されてしまう
  * スプレッドシート取得時のIDと、レポート作成ボタンを押した時点のIDでそれぞれコメントデータが保存される
  * ID変更前のデータはその後参照されず、APIサーバーのディスク容量を無駄に消費してしまう


# 提案内容
* データ取得後にレポートのIDを変更できないようにした上で、画面上でその旨を表示する
  * e.g. 「スプレッドシートからデータを取得した後はIDを変更できません」といった文言をIDの入力フォーム直下に表示する

ただ、容量の問題を解決するだけであれば、report_status.jsonに存在しないslugのデータがinputsに存在する場合に削除するような処理を走らせるようにしても良いかもしれない？ 妙案ある方はコメントいただけると助かります。




**コメント:**

- **nasuka** (2025-03-26T07:12:30Z):

* 起こっている問題はデータの二重保管
* データ取得後もIDを変更できたほうがユーザビリティは良い

ので、IDを変更できないようにするよりは無駄に作成されてしまったデータを削除する方針の方が良いかも

- **nishio** (2025-03-26T08:12:48Z):

そもそ大きなデータでも100MBくらいのものなので、重複保存されても大した問題ではない気がします。

>データ取得後もIDを変更できたほうがユーザビリティは良い

ここは間違いなくそうだと思いました。

- **shingo-ohki** (2025-03-26T09:53:18Z):

/assign

---

### [[FEATURE]resultをローカル環境へ取得するscriptをつくる](https://github.com/digitaldemocracy2030/kouchou-ai/issues/179)

**作成者:** nishio  
**作成日:** 2025-03-25T13:23:48Z  
**内容:**

# 背景

リモート環境で作成されたレポートのデータをローカルに持ってくることが現状少し不便

>1.既存のAPIに対して以下を実施
GET /reports を叩いて全レポートのslugを取得する
GET /reports/{slug}を叩いて個別のレポートのresultを取得する
2.新規に構築した環境に以下を実施
outputs配下に各slugの名称でディレクトリを作ってその配下にresultを置く
./server/data/配下のreport_status.jsonを手動で編集する（これを編集しないと一覧画面にレポートが表示されない）

from https://w1740803485-clv347541.slack.com/archives/C08F7JZPD63/p1742904758383619?thread_ts=1742889178.309719&cid=C08F7JZPD63


# 提案内容
これをやるscriptを作る


**コメント:**

- **nasuka** (2025-03-25T13:55:38Z):

@nishio 

> ./server/data/配下のreport_status.jsonを手動で編集する（これを編集しないと一覧画面にレポートが表示されない）

この部分について補足で、report_status.jsonは  `GET /reports` で取得した情報を少し加工すると作ることができます。

`GET /reports`  のレスポンスは次のような形式で、

```
[
  {
    "slug": "example11",
    "title": "example",
    "description": "example",
    "status": "ready"
  },
  {
    "slug": "example2",
    "title": "aaaa",
    "description": "bbbb",
    "status": "ready"
  }
]
```


report_status.jsonは次のような形式になっており、APIで取得した値をslugの情報をkeyとするようなjsonに加工することでreport_status.jsonの形式にすることができます。
```
{
    "example11": {  // keyはslugが入る
        "slug": "example11",
        "status": "ready",
        "title": "example",
        "description": "example"
    },
    "example2": {
        "slug": "example2",
        "status": "ready",
        "title": "aaaa",
        "description": "bbb"
    }
}
```

- **nasuka** (2025-03-25T14:12:52Z):

あ、すでにPRを送ってましたね（見落としてました
↑はご放念ください 🙇 

---

### [[FEATURE]dependabotの導入](https://github.com/digitaldemocracy2030/kouchou-ai/issues/151)

**作成者:** nasuka  
**作成日:** 2025-03-25T05:54:10Z  
**内容:**

# 背景
* セキュリティの脆弱性に伴うパッケージのアップデートを行いたい
* 現状でもgithub上の `Security` でアラートはくるが、パッケージアップデートをする際は手作業が入る


# 提案内容
* dependabotを用いてパッケージアップデートのPR作成を自動化する

**コメント:** なし

---

### [[FEATURE]API呼び出し前にCSVファイル内の意見数を確認する](https://github.com/digitaldemocracy2030/kouchou-ai/issues/147)

**作成者:** ei-blue  
**作成日:** 2025-03-25T05:27:30Z  
**内容:**

# 背景
CSVファイルのデータから最終的に抽出された意見の数が詳細設定で設定されたクラスタ数を下回っていると、クラスタリングの過程でエラーになり、無駄にAPIを呼び出すことになってしまう。

# 提案内容
「レポート作成を開始」ボタンを押した際にクラスタ設定の数とCSVファイルの行数を比較し、CSVファイルの行数の方が少ない場合に警告を出す。
コメント数（CSVファイルの行数）＝最終的な意見の数　ではないため、エラーにする必要はない。

**コメント:**

- **ei-blue** (2025-03-25T05:27:39Z):

/assign

---

### [[BUG] Unknown event handler property `onFileRemove`. が出る](https://github.com/digitaldemocracy2030/kouchou-ai/issues/142)

**作成者:** shingo-ohki  
**作成日:** 2025-03-25T03:25:55Z  
**内容:**

### 概要

https://github.com/digitaldemocracy2030/kouchou-ai/commit/685bb7c685e281ad3afb760bc8e7c9d649532d41

の状態のコードで localhost:4000/create にアクセスすると以下のエラーが出る。

`Unknown event handler property `onFileRemove`. It will be ignored.
`
### 再現手順

1. https://github.com/digitaldemocracy2030/kouchou-ai/commit/685bb7c685e281ad3afb760bc8e7c9d649532d41 を checkout
2. docker compose up
3. ブラウザで localhost:4000/create にアクセス

### 期待する動作
エラーが出ないこと

### スクリーンショット・ログ

![Image](https://github.com/user-attachments/assets/71256468-62ea-40fe-aa58-ccfbbe88199f)

![Image](https://github.com/user-attachments/assets/55429512-79dc-4dd6-8bbe-a6d0b5ee98a0)

### その他

<!-- 追加で伝えておきたいことがあれば記入してください -->

**コメント:**

- **shingo-ohki** (2025-03-25T03:26:58Z):

/assign

---

### [テスト](https://github.com/digitaldemocracy2030/kouchou-ai/issues/135)

**作成者:** nasuka  
**作成日:** 2025-03-23T02:33:21Z  
**内容:**

## 要望内容
テスト

---
こちらのイシューはGoogle Form経由で投稿されたものです

**コメント:** なし

---

### [テスト用イシューです](https://github.com/digitaldemocracy2030/kouchou-ai/issues/134)

**作成者:** nasuka  
**作成日:** 2025-03-23T02:33:18Z  
**内容:**

## 要望内容
テスト

---
こちらのイシューはGoogle Form経由で投稿されたものです

**コメント:** なし

---

### [[DOCUMENT]Azureのセットアップガイドに関する免責事項を記載する](https://github.com/digitaldemocracy2030/kouchou-ai/issues/133)

**作成者:** nasuka  
**作成日:** 2025-03-23T02:11:50Z  
**内容:**

# 現在の問題点
- セットアップ手順に従った結果に対する責任範囲が明確に定義されていない
  - 利用者がトラブル発生時にプロジェクトに過度な責任を求める可能性がある

# 提案内容
以下のような免責事項を記載する

* 本ドキュメントは情報提供のみを目的としており、特定の環境でのデプロイを保証するものではありません。
* 本ガイドに従って実施されたデプロイや設定によって生じた問題、損害、セキュリティインシデントについて、作者および関連プロジェクト貢献者は一切の責任を負いません。
* 各組織のセキュリティポリシーやコンプライアンス要件に従って適切に評価・カスタマイズしてください。


**コメント:**

- **nasuka** (2025-03-23T02:13:42Z):

https://github.com/digitaldemocracy2030/kouchou-ai/pull/115
のmerge後に対応する

---

### [[FEATURE] OpenRouterを用いて動くようにする](https://github.com/digitaldemocracy2030/kouchou-ai/issues/128)

**作成者:** 101ta28  
**作成日:** 2025-03-22T14:07:01Z  
**内容:**

# 背景
[idobata-analyst](https://github.com/digitaldemocracy2030/idobata-analyst) では、AI呼び出しに[OpenRouter](https://openrouter.ai)を用いている。

環境構築時に共通プラットフォームのKeyを用いることができれば便利だと思うため。

また、(OpenAI以外の)複数モデルの切り替えがしやすいものが良いと思ったため。

# 提案内容

server ディレクトリ内の`config.py`や`hierarchical_utils.py`を変更すれば動くと思われます。

**コメント:**

- **nishio** (2025-03-22T14:13:11Z):

embeddingとextractionからの呼び出しはservice/llm.pyに集約されつつあって、そこで環境変数を読んでAzure OpenAI Serviceと切り替えているので、そこにOpenRouterも追加すると言うのは手だと思います

- **101ta28** (2025-03-22T14:38:07Z):

/assign

- **101ta28** (2025-03-22T16:54:28Z):

悲しいかな OpenRouter は embedding 非対応なので、そこは OpenAI or Azure 頼みですね...

issue立てましたが、どっちみちOpenAIに頼ってしまう形になるので、closeしたほうが良いかもしれないです。

OpenRouterがembedding対応したら変更とかで良さそう...

- **nishio** (2025-03-22T17:27:30Z):

なるほど、じゃあ一旦wontfixにしてみます

- **blu3mo** (2025-03-23T06:16:56Z):

文脈を補完しておくと、いどばたでOpenRouterを使い始めた一番の理由は「Google Gemini APIだとrate limitを上げるのが面倒だが、Open Routerはお金さえ入れればrate limitを上げられるから」です

---

### [[FEATURE]Shift-JISのcsvをUTF-8に変更する](https://github.com/digitaldemocracy2030/kouchou-ai/issues/124)

**作成者:** yuneko1127  
**作成日:** 2025-03-22T04:56:29Z  
**内容:**

# 背景
<!-- なぜその機能が必要なのか、何が改善されるのか具体的に記入してください -->
ExcelなどでCSVを作成するとShift-JISになり、非エンジニアの利用を考えるのであれば、文字コードの変換は利用者側ではなくシステム側でやるべきだと考えるから。


# 提案内容
<!-- 実装案やデザイン案があれば記入してください -->
最初にcsvを読んでいるところで、UTF-8でない場合は別の処理をする。

**コメント:**

- **yuneko1127** (2025-03-22T04:57:14Z):

/assign

---

### [[FEATURE]文字コードがSJISやBOMがついてるときPythonで変換する](https://github.com/digitaldemocracy2030/kouchou-ai/issues/123)

**作成者:** nishio  
**作成日:** 2025-03-22T04:50:42Z  
**内容:**

# 背景
ExcelからCSVを書き出す時、だいたいSJISで書き出してしまうしUTF-8にするとしてもBOMをつけてしまったりする

# 提案内容
エラーにするより、しれっと変換したほうが説明コスト低いのではないか


**コメント:**

- **nishio** (2025-03-22T08:09:22Z):

duplicate

---

### [[FEATURE]サンプルデータの件数増加](https://github.com/digitaldemocracy2030/kouchou-ai/issues/120)

**作成者:** nasuka  
**作成日:** 2025-03-21T12:59:17Z  
**内容:**

# 背景
- 現在のサンプルは50件しかないため、濃いクラスタを表示しても全体図と描画が変わらず挙動のイメージがつかない


# 提案内容
- サンプルデータの件数を増やす
  - 200件程度あれば良さそう

**コメント:**

- **nishio** (2025-03-21T15:41:17Z):

「生成されたレポートを見て挙動のイメージがつく」と言う目的ではそもそもサンプルデータを増やすより、大規模データで作ったレポートを静的ホストして誰でも見れるようにするのが良さそう

- **nasuka** (2025-03-21T16:33:21Z):

なるほど、サンプルデータはcsvフォーマットを確認するために用意しているのであって、動作のイメージ確認はデモ環境などを見てもらった方が良いのではないかということですかね。

自分としては、 とりあえずサンプルデータで出力を試すという人は一定存在する印象があり、
その結果が微妙だとプロダクトに対してネガティブなイメージを抱かれてしまう可能性があるので、サンプルデータであってもある程度はまともにクラスタが形成されるデータの方が望ましいように思います。
今のサンプルだと2層目のクラスタ数のデフォルト値では50件のデータに対して50クラスタが形成されてしまう（つまり実質的に2層目はデータ点がそのままクラスタになる）ので、少なくともまともにクラスタができる程度には件数があった方が良いのではないかと思いました（フォーマットのサンプルとしては今のままでも問題ないですが、まともなレポートを作るサンプルとしては不十分なので）
あとは、デフォルトのモデル（gpt-4o-mini）を使うのであればコストもそこまで高くならないので、件数が増えるデメリットよりはメリットの方が大きいように思いました。



- **nishio** (2025-03-22T00:17:25Z):

50件だとせっかく作った階層クラスタリングがテストできないわけなんですね、なるほど納得です

---

### [[REFACTOR]レポート画面における「議論」という言葉がわかりにくい](https://github.com/digitaldemocracy2030/kouchou-ai/issues/118)

**作成者:** nasuka  
**作成日:** 2025-03-21T08:20:23Z  
**内容:**

# 背景
* レポート表示画面で「議論」という単語が使われているが、日本語としてわかりにくい
  * 「33議論」といった表記はそもそも日本語として正しくないように思える
  * Analysis配下の「議論を抽出」といった表現も違和感がある
![Image](https://github.com/user-attachments/assets/d4068108-dc0c-4639-9dae-942ab870db3a)



![Image](https://github.com/user-attachments/assets/669b7198-8e0f-43ed-a4ad-dbbad40c5720)

# 提案内容
1. クラスタタイトル下の「33議論」等の表現は「33件」という表現に変える
2. Analysis内で使われている「議論」という単語は 「意見」に置き換える（実際に行っている処理としても意見の方がニュアンス的に正しい）


**コメント:**

- **shingo-ohki** (2025-03-28T06:10:29Z):

/assign

---

### [[FEATURE]クラスタ数5/50が分数に見える](https://github.com/digitaldemocracy2030/kouchou-ai/issues/114)

**作成者:** nishio  
**作成日:** 2025-03-20T12:24:41Z  
**内容:**

# 背景

<img width="817" alt="Image" src="https://github.com/user-attachments/assets/4adeaef8-77dc-4dbb-a8d9-44f7b2e2fe4c" />

実際には「一段階目5個、二段階目50個」の意味だが、まあこの表現では伝わらないか...


# 提案内容
たとえば「一段階目5件 / 二段階目50件」とか「大分類5 / 小分類50」とかの文字を補う

**コメント:**

- **nasuka** (2025-03-26T11:49:30Z):

/ではなく→に変えるとよいのではないか？

- **takahiroanno** (2025-03-26T11:50:20Z):

例：
5 → 50

- **nishio** (2025-03-26T15:28:29Z):

https://github.com/digitaldemocracy2030/kouchou-ai/pull/188

---

### [[REFACTOR] 「クラスタ」言い換え案](https://github.com/digitaldemocracy2030/kouchou-ai/issues/110)

**作成者:** nishio  
**作成日:** 2025-03-20T12:05:11Z  
**内容:**

# 現在の問題点
「クラスタ」という言葉がわかりにくい

# 提案内容
案出し
- 意見集団
- 意見グループ
- 意見チーム

**コメント:**

- **takahiroanno** (2025-03-20T13:39:37Z):

意見グループ、に一票

- **shingo-ohki** (2025-03-25T03:55:29Z):

/assign

---

### [[FEATURE]ロゴから掛け算をなくす](https://github.com/digitaldemocracy2030/kouchou-ai/issues/106)

**作成者:** takahiroanno  
**作成日:** 2025-03-20T07:59:47Z  
**内容:**

# 背景

![Image](https://github.com/user-attachments/assets/df86ddf6-c54f-492c-b12d-4ee177281817)

- 上記ロゴの掛け算の右側はないほうがよいかと思います
  - 自治体、政党などがより使いやすくなる
  - ユーザーにとっても初見で情報が多すぎなくて済む

フッターの右下にデジ民の解説はあるので、ここに入れずに済むかと思います

# 提案内容
掛け算の右側の削除

**コメント:**

- **101ta28** (2025-03-22T12:09:01Z):

/assign

---

### [[FEATURE]CSVのアップロードが成功した際に成功メッセージを表示](https://github.com/digitaldemocracy2030/kouchou-ai/issues/100)

**作成者:** ei-blue  
**作成日:** 2025-03-20T06:36:54Z  
**内容:**

# 背景
新規レポート作成画面において、現状ではCSVをアップロードした際にファイルアップロードエリアの下にファイル名が表示されるが、操作画面のサイズによってはスクロールしないと見えない位置にあり、ファイルがアップロードできたかどうかわかりにくい。

![Image](https://github.com/user-attachments/assets/35d419bb-4685-4124-bb71-34d59235281c)


# 提案内容

やり方はいろいろありそうなのでこだわらないです。以下はパッと思いついた例。

- 「ファイルがアップロードされました」というフラッシュメッセージを出す
- ファイルアップロードエリアの縦幅を小さくする
- アップロード成功時にファイルアップロードエリアの文言を変える

**コメント:**

- **nishio** (2025-03-21T15:51:41Z):

複数件アップロードされても処理できない現状、ドロップターゲットが非表示になったほうがいい気がしました。

- **101ta28** (2025-03-24T12:23:09Z):

/assign

---

### [[FEATURE] Azure で動作させる](https://github.com/digitaldemocracy2030/kouchou-ai/issues/94)

**作成者:** shingo-ohki  
**作成日:** 2025-03-19T01:40:31Z  
**内容:**

# 背景
#80 自治体や大企業などを中心にAzureを使いたいというニーズがある

# 提案内容
Azure Container Apps で動作させる

**コメント:**

- **shingo-ohki** (2025-03-19T01:58:21Z):

素人からするとハマりポイントはここっぽい
`NEXT_PUBLIC_*` の環境変数は、ビルド時に指定する必要がある

- **shingo-ohki** (2025-03-19T14:03:38Z):

ひとまずメモ
https://gist.github.com/shingo-ohki/6163d2c599b6d34795a21761ac6d1dae

この辺が関係ありそう
https://nextjs.org/docs/pages/building-your-application/configuring/environment-variables#runtime-environment-variables


- **shingo-ohki** (2025-03-20T05:07:52Z):

この [Makefile](https://gist.github.com/shingo-ohki/6163d2c599b6d34795a21761ac6d1dae) で
```
export OPENAI_API_KEY=your_api_key_here

make azure-login

make azure-setup-all
```

で Azure に環境ができてレポート生成もできるところまではできる。

が、しばらくすると多分 healthcheck でコンテナが落ちて、今はまだレポートが永続化されないからまっさらになってしまう？

- **shingo-ohki** (2025-03-20T14:56:31Z):

healthcheck の設定方法が分かり、それでうまく動いていそうなので、
明日改めて最初から処理がすべて動くか確認する。
それで問題なければ Pull Request を出す予定

---

### [[FEATURE]hierarchical initial labelling, merge labellingの並列化](https://github.com/digitaldemocracy2030/kouchou-ai/issues/93)

**作成者:** nasuka  
**作成日:** 2025-03-18T09:43:50Z  
**内容:**

# 背景
* クラスタのラベリング処理の動作が遅い
  * ラベリング時にOpenAI APIにリクエストを投げる処理が、（実質的に）並列実行されていないため
  * コードとしては並列実行できるようになっているが、並列数がデフォルト値（1）でのみ実行されるようになっているため、実質的に並列で処理されない


# 提案内容
* ダッシュボード側で並列数を入力する
  * 参考: https://github.com/digitaldemocracy2030/kouchou-ai/issues/92
    * 並列数自体は、extraction等と共通のものを使い回すのが良さそう（個別に並列数を設定するのは複雑すぎる）
* バックエンド側でconfig保存時にinitial labelling/merge labellingそれぞれで並列数を保存する
  * https://github.com/digitaldemocracy2030/kouchou-ai/blob/d872198477e1f5a9a7db782eb74c0323b49d9119/server/src/services/report_launcher.py#L21-L29

**コメント:**

- **nishio** (2025-03-21T15:54:53Z):

API Keyを作ったばっかりの人のTierが低くてRate Limitにぶつかる問題はありますけど、ユースケースの大部分は並列化して良いものだと思うので並列化したほうが平均的な効用が大きそうですね。

あ、Tier低い人のケアはここにも書いてあった: https://github.com/digitaldemocracy2030/kouchou-ai/issues/92

---

### [[FEATURE]OpenAI API実行時のworker数をレポート作成時に設定できるようにしたい](https://github.com/digitaldemocracy2030/kouchou-ai/issues/92)

**作成者:** nasuka  
**作成日:** 2025-03-18T09:34:49Z  
**内容:**

# 背景
* バックエンドでレポート出力時に実行しているextraction処理は、並列でOpenAI APIを呼び出している
* 現在は並列実行数は30で固定されているが、OpenAI アカウントのtierによってはより大きくする余地がある


# 提案内容
* 管理画面において、レポート作成時の詳細設定で並列実行数を入力できるようにする
  * 今のところ特に問題は起きてないので、デフォルトは30で良さそう
* バックエンド側でconfigを保存する際に、受け取ったworker数を保存する
  * 参考: https://github.com/digitaldemocracy2030/kouchou-ai/blob/d872198477e1f5a9a7db782eb74c0323b49d9119/server/src/services/report_launcher.py#L21

**コメント:** なし

---

### [[FEATURE] 分析手順を非表示にする](https://github.com/digitaldemocracy2030/kouchou-ai/issues/83)

**作成者:** nanocloudx  
**作成日:** 2025-03-18T03:52:42Z  
**内容:**

# 背景
Analysis の分析手順の項目は、より詳細を知りたい人向けの情報である
詳細設定や専門家向けの情報は、あえて隠すことで多くの人にわかりやすい印象を与える（と主観的に考えています）

# 提案内容
「分析手順を表示」みたいなボタンでアコーディオン表示する
`<Presence />` コンポーネントが役立ちます

**コメント:**

- **shgtkshruch** (2025-03-23T03:46:55Z):

/assign

---

### [[FEATURE]Plotly UIの日本語化](https://github.com/digitaldemocracy2030/kouchou-ai/issues/82)

**作成者:** nishio  
**作成日:** 2025-03-18T03:50:46Z  
**内容:**

# 背景

>安野貴博
>これ日本語化してあげたい
>![Image](https://github.com/user-attachments/assets/08427c7c-5793-4053-b40d-049502872b39)

# 提案内容

AIいわく日本語ロケールの設定をすればいいらしい:

plotly-locale-ja.jsファイルは、Plotlyの公式リポジトリから取得できます。以下の手順で入手できます：

1. Plotly.jsのGitHubリポジトリにアクセス: https://github.com/plotly/plotly.js
2. dist/localesディレクトリ内のja.jsファイルをダウンロード: https://github.com/plotly/plotly.js/blob/master/dist/plotly-locale-ja.js
3. このファイルをclient/public/jsディレクトリに配置

このファイルはPlotlyチャートのUIテキスト（ボタンラベル、ツールチップなど）を日本語に翻訳するための設定ファイルです。

**コメント:**

- **101ta28** (2025-03-22T13:36:54Z):

/assign

- **101ta28** (2025-03-24T02:29:59Z):

Pull Requestとの関連付けが抜けていました！

手動でのCloseお願いしてもよろしいでしょうか？

---

### [[FEATURE]ソフト404問題の改善](https://github.com/digitaldemocracy2030/kouchou-ai/issues/69)

**作成者:** nanocloudx  
**作成日:** 2025-03-16T16:59:43Z  
**内容:**

# 背景
現在は存在しないレポートURLを開こうとするとエラー表示となるが、HTTP200でレスポンスしてしまっている

# 提案内容
適切に404をレスポンスするように修正する

**コメント:**

- **nanocloudx** (2025-03-16T17:00:30Z):

この Issue はおそらく https://github.com/takahiroanno2024/kouchou-ai/issues/61 にも関連します

- **nishio** (2025-03-17T03:13:27Z):

from https://w1740803485-clv347541.slack.com/archives/C08F7JZPD63/p1742127316084179?thread_ts=1742111805.793019&cid=C08F7JZPD63

ISRでデータが無い場合のキャッシュ防止: Next.jsのISRでは、一度生成したページは指定時間キャッシュされます。したがって、データ取得に失敗して「エラーページ」や空ページを生成してしまうと、そのページが次の再検証までキャッシュされてしまいます[zenn.dev](http://zenn.dev/)
。この問題を避けるには、データが無い場合はページを生成しない工夫が必要です。具体的には、getStaticProps内でデータが取得できなかった場合に**notFound: true**を返す方法があります[nextjs.org](http://nextjs.org/)
。notFound: trueを返すとそのリクエストは404ページになりますが、後述のとおり再検証（revalidate）を組み合わせることで後からデータが追加された際にページを再生成できます[zenn.dev](http://zenn.dev/)
。また、データ無しの場合だけ非常に短いrevalidate時間を設定し、次回リクエスト時に即再取得させる方法もあります（例: データ無し時はrevalidate: 5秒に設定する）[dev.to](http://dev.to/)
。このようにすることで、データが用意できていない間は頻繁に再検証を行い、データが揃い次第最新ページを配信できます。公式ドキュメントでも、ユーザ生成コンテンツの削除などに対応するためnotFoundとISR（revalidate）の併用が可能であると説明されています[nextjs.org](http://nextjs.org/)
。

- **shgtkshruch** (2025-03-25T09:07:06Z):

/assign

---

### [[FEATURE]ツリーマップで各クラスタの件数を表示する](https://github.com/digitaldemocracy2030/kouchou-ai/issues/17)

**作成者:** nasuka  
**作成日:** 2025-03-04T11:35:12Z  
**内容:**

# 背景
* クラスタ毎に何件あるのかを把握したい

# 提案内容
* ツリーマップ上で件数を表示する
  * 現状はパーセンテージのみを表示しているが、合わせて件数も表示したい

![Image](https://github.com/user-attachments/assets/029763cc-e763-443b-8d4b-c946f1e3df7f)

**コメント:**

- **shgtkshruch** (2025-03-22T06:26:22Z):

/assign

---

## 過去1週間に作成されたissue (28件)

### [[BUG]静的HTML出力時の画像の 404 解消](https://github.com/digitaldemocracy2030/kouchou-ai/issues/196)

**作成者:** nishio  
**作成日:** 2025-03-28T15:41:33Z  
**内容:**

### 概要
see https://github.com/digitaldemocracy2030/kouchou-ai/pull/195
<!-- バグの簡潔な説明をお願いします -->

### 再現手順

1. <!-- バグが再現する手順をステップごとに記入してください -->
2. 
3. 

### 期待する動作

<!-- 本来どう動作すべきかを記入してください -->

### スクリーンショット・ログ

<!-- 必要に応じてスクリーンショットやエラーログなどを添付してください -->

### その他

<!-- 追加で伝えておきたいことがあれば記入してください -->

**コメント:**

- **shgtkshruch** (2025-03-28T23:36:42Z):

/assign

---

### [[DOCUMENT] 環境変数を書き換えた場合は docker compose up --build を実行するようにREADMEに追記する](https://github.com/digitaldemocracy2030/kouchou-ai/issues/191)

**作成者:** nasuka  
**作成日:** 2025-03-28T06:16:48Z  
**内容:**

# 現在の問題点
* 環境変数を変更した場合はdocker imageをbuildしなおさないと動作しないケースがある
  * フロントでは、APIキーなどの一部の環境変数をimageのビルド時に埋め込んでいる
  * このため、フロント側はdocker compose upを実行すると初回に設定した環境変数のイメージのままコンテナが立て続けられてしまう（ビルド時に埋め込んでいる環境変数は、イメージをビルドし直さない限り.envを編集しても変更が反映されない）
    * これにより以下の様にapiとフロントのAPIキーが一致しないケースが発生してしまう

```
1: デプロイの作業をしてたディレクトリでそのまま新機能開発をしようとしてdocker-compose upしたら起動はしたけど管理画面がAPIサーバに繋がらなくてスピナーが回りっぱなし
2: 原因は401 unauthorized
3: docker-compose upすると、compose.yamlのclient-adminはAPIサーバに接続するためのAPIキーをargsでハードコードしているので管理画面には古いキーが環境変数として渡される、一方でserverの方はそれをしないで.envを渡しているのでこちらは新しいAPIキーが渡される、不一致なので繋がらない
```

# 提案内容
* 環境変数を書き換えた場合は `docker compose up --build` を実行するようにREADMEに追記する


**コメント:** なし

---

### [[FEATURE]1回のextractionで複数のcommentを処理する](https://github.com/digitaldemocracy2030/kouchou-ai/issues/190)

**作成者:** nasuka  
**作成日:** 2025-03-28T02:12:39Z  
**内容:**

# 背景
* 現在のextraction処理は1リクエストに1件のコメントを処理しているため、実行に時間がかかる
  * リクエストそのものの並列化は行われているが、OpenAI APIのrate limitの関係で並列化による高速化も限界がある


# 提案内容
* 1回のextractionで複数のコメントを同時に処理する
  * 同時処理の件数が増えることで、rate limit(requests per minute)の問題が緩和される

プロンプトのイメージ
```
あなたは専門的なリサーチアシスタントで、整理された議論のデータセットを作成するお手伝いをする役割です。
人工知能に関する公開協議を実施した状況を想定しています。一般市民から寄せられた議論の例を提示しますので、それらをより簡潔で読みやすい形に整理するお手伝いをお願いします。必要な場合は2つの別個の議論に分割することもできますが、多くの場合は1つの議論にまとめる方が望ましいでしょう。
結果は出力例に記載したjson形式で出力して

## 入力例
- id1: AIは仕事の効率化に役立つ。人生の相談相手にもなってくれる。
- id2: AIは電力を消費しすぎる問題がある
- id3: AIには反対です

## 出力例
{
    "id1": [
        "AIは仕事の効率化に役立つ",
        "AIは人生の相談相手になる"
    ],
    "id2": [
        "AIは電力消費が大きい"
    ],
    "id3": [
        "AIには反対"
    ]
}
```

extraction実行時のLLMのresponse formatが変わるため、周辺の実装も変える必要がある。

## 進め方
* まずは、上記のようなプロンプト・出力フォーマットに変更して同時処理数を増やした場合にどのようにアウトプットの文言が変わるかを確認する
  * 入力データは、ツイートレベルの長さのケースと、aipubcomのように1コメントが長いケースの両方で確かめた方が良さそう
* 抽出結果が問題なさそうであればプロダクトに機能実装する


**コメント:** なし

---

### [[FEATURE]CSVをJSONに変換せずに送信したい](https://github.com/digitaldemocracy2030/kouchou-ai/issues/186)

**作成者:** ei-blue  
**作成日:** 2025-03-26T08:36:06Z  
**内容:**

# 背景

- 現在、コメントデータはフロントエンドでCSVファイルを読み込んだ後、JSONに変換し、comments 配列としてAPIに送信している。
- しかし、これはデータ量が多い場合に通信サイズやメモリ使用量が増える原因となり、効率的ではない。
- また、バックエンド側でも最終的にはCSV形式に戻して処理しているため、変換処理が冗長。

# 提案内容

- CSVファイルをフロントエンドからそのままAPIに送信できるように変更し、サーバー側で直接ファイルを受け取って処理できるようにする。
- これにより、クライアント側の前処理やメモリ消費を削減でき、処理効率が向上。

想定される実装方法：

- フロントエンドでは FormData を使ってCSVファイルを直接送信
- バックエンドでは UploadFileなどを使ってCSVファイルを受け取り、既存の inputs/xxx.csv に保存する

## 留意事項

- 現在フロントエンドで簡単なバリデーションを行っているが、これは最終的にはなくし、フロントエンドの処理を軽くする
- コメントIDの生成もフロントエンドで行っているのでそれも必要に応じてサーバーに移す
- スプレッドシートを入力として受け取る #132 の動きも気にしておく


**コメント:** なし

---

### [[FEATURE]失敗したプロセスの詳細情報を得られるようにする](https://github.com/digitaldemocracy2030/kouchou-ai/issues/185)

**作成者:** nishio  
**作成日:** 2025-03-26T07:34:45Z  
**内容:**

# 背景

NISHIO Hirokazu
うーん、「成功して完了したレポートの結果」をローカルにコピーできるようにはなったけど、デプロイしてる本番環境をユーザが使ってなんかコケたというときに、どんなデータを入れてどこまで進んでどんな死に方をしたのかを確認できないと捗らないな。本番環境のコンテナに直接入ったりサーバのログを見たりすればなんとかなるとはいえ、さっと手元に落として確認したい。やっぱりzipしてダウンロードするAPIをつけるべきか？？
2 件の返信

Nasuka Sumino
あっても良いと思います！
他にもいくつかアプローチはある気がしつつ（ステータスを細分化する、外部ストレージ連携してストレージを見に行く等）、データを丸ごと落とせるようにするのが実装的にも比較的ライトで原因究明もしやすいように思います。 

NISHIO Hirokazu
今回、aipubcomの現時点で公開されてる7つのPDFから過去最大のデータセットを作って入れてみたんですけど、たくさん時間が掛かってから死んだので雰囲気的にembeddingは完了してからクラスタリング時に何か起きたのかなぁみたいな気持ちです

https://w1740803485-clv347541.slack.com/archives/C08F7JZPD63/p1742971649061709

# 提案内容

<img width="319" alt="Image" src="https://github.com/user-attachments/assets/78faf532-a481-4dbb-8279-17fe42cf258d" />

管理画面の...ボタンで出るメニューに中間データなどをまとめたzipをダウンロードする機能をつける

**コメント:**

- **nishio** (2025-03-26T07:35:25Z):

一旦もう少し詳細化してみます

---

### [[FEATURE]スプレッドシートでデータを取得した後にレポートIDを変更して作成を実行するとコメントデータが二重に保管される](https://github.com/digitaldemocracy2030/kouchou-ai/issues/184)

**作成者:** nasuka  
**作成日:** 2025-03-26T06:42:10Z  
**内容:**

# 背景
* レポート作成画面において、スプレッドシートからデータを取得した後にレポートのIDを変更すると、コメントのデータが二重に保管されてしまう
  * スプレッドシート取得時のIDと、レポート作成ボタンを押した時点のIDでそれぞれコメントデータが保存される
  * ID変更前のデータはその後参照されず、APIサーバーのディスク容量を無駄に消費してしまう


# 提案内容
* データ取得後にレポートのIDを変更できないようにした上で、画面上でその旨を表示する
  * e.g. 「スプレッドシートからデータを取得した後はIDを変更できません」といった文言をIDの入力フォーム直下に表示する

ただ、容量の問題を解決するだけであれば、report_status.jsonに存在しないslugのデータがinputsに存在する場合に削除するような処理を走らせるようにしても良いかもしれない？ 妙案ある方はコメントいただけると助かります。




**コメント:**

- **nasuka** (2025-03-26T07:12:30Z):

* 起こっている問題はデータの二重保管
* データ取得後もIDを変更できたほうがユーザビリティは良い

ので、IDを変更できないようにするよりは無駄に作成されてしまったデータを削除する方針の方が良いかも

- **nishio** (2025-03-26T08:12:48Z):

そもそ大きなデータでも100MBくらいのものなので、重複保存されても大した問題ではない気がします。

>データ取得後もIDを変更できたほうがユーザビリティは良い

ここは間違いなくそうだと思いました。

- **shingo-ohki** (2025-03-26T09:53:18Z):

/assign

---

### [[FEATURE]resultをローカル環境へ取得するscriptをつくる](https://github.com/digitaldemocracy2030/kouchou-ai/issues/179)

**作成者:** nishio  
**作成日:** 2025-03-25T13:23:48Z  
**内容:**

# 背景

リモート環境で作成されたレポートのデータをローカルに持ってくることが現状少し不便

>1.既存のAPIに対して以下を実施
GET /reports を叩いて全レポートのslugを取得する
GET /reports/{slug}を叩いて個別のレポートのresultを取得する
2.新規に構築した環境に以下を実施
outputs配下に各slugの名称でディレクトリを作ってその配下にresultを置く
./server/data/配下のreport_status.jsonを手動で編集する（これを編集しないと一覧画面にレポートが表示されない）

from https://w1740803485-clv347541.slack.com/archives/C08F7JZPD63/p1742904758383619?thread_ts=1742889178.309719&cid=C08F7JZPD63


# 提案内容
これをやるscriptを作る


**コメント:**

- **nasuka** (2025-03-25T13:55:38Z):

@nishio 

> ./server/data/配下のreport_status.jsonを手動で編集する（これを編集しないと一覧画面にレポートが表示されない）

この部分について補足で、report_status.jsonは  `GET /reports` で取得した情報を少し加工すると作ることができます。

`GET /reports`  のレスポンスは次のような形式で、

```
[
  {
    "slug": "example11",
    "title": "example",
    "description": "example",
    "status": "ready"
  },
  {
    "slug": "example2",
    "title": "aaaa",
    "description": "bbbb",
    "status": "ready"
  }
]
```


report_status.jsonは次のような形式になっており、APIで取得した値をslugの情報をkeyとするようなjsonに加工することでreport_status.jsonの形式にすることができます。
```
{
    "example11": {  // keyはslugが入る
        "slug": "example11",
        "status": "ready",
        "title": "example",
        "description": "example"
    },
    "example2": {
        "slug": "example2",
        "status": "ready",
        "title": "aaaa",
        "description": "bbb"
    }
}
```

- **nasuka** (2025-03-25T14:12:52Z):

あ、すでにPRを送ってましたね（見落としてました
↑はご放念ください 🙇 

---

### [[BUG]パスワードに&があるとそこでコマンドが分割される](https://github.com/digitaldemocracy2030/kouchou-ai/issues/177)

**作成者:** nishio  
**作成日:** 2025-03-25T08:44:36Z  
**内容:**

### 概要
`ADMIN_API_KEY=foo&bar` のようなときに実行されるコマンドが `command --ADMIN_API_KEY=foo&bar`になって、それは`ADMIN_API_KEY=foo` と `bar`が`&`で繋がれたものと認識されてしまう

### 期待する動作

`command --ADMIN_API_KEY="foo&bar"`になる

### その他

まあ、記号を使わないだけで回避できるので緊急というわけではない、気づいたときに書かないと忘れるので...

**コメント:** なし

---

### [[FEATURE]LLMベースの分類機能の実装](https://github.com/digitaldemocracy2030/kouchou-ai/issues/176)

**作成者:** nasuka  
**作成日:** 2025-03-25T08:30:43Z  
**内容:**

# 背景
* 既存の階層クラスタリングアルゴリズムは以下の課題がある
  * ある程度データの件数が存在することを前提としている（小規模データだとワークしにくい）
  * embeddingに基づいてデータをまとめているため、クラスタリングの品質がembedding（およびUMAP後の2次元ベクトル）の品質に依存する


# 提案内容
LLMベースの分類機能を実装する。これは以下の2つの方向性がある。

1. 分類するトピックをLLMで自動で構築するパターン
  a. データから、どのようなトピックがあるかを自動で推定し、各意見をトピックに分類する
  b. 参考: [sensemaking](https://medium.com/jigsaw/making-sense-of-large-scale-online-conversations-b153340bda55)
2. 分類するトピックを人間が付与するパターン
  a. 意見を所与のトピックに分類する
  b. あらかじめ決められたトピックに意見を分類したい場合に活用できる

あった方が良い機能であるように思う一方で、既存のクラスタリングベースのアルゴリズムとこの機能をどう同居させるかが悩ましい。
既存のレポートは見せ方も異なってくると思われるので、別形式のページを出力するのが一案。

# 進め方について
* いきなり機能を実装するのではなく、プロダクトとは独立して実験スクリプトを実装し、検証用のデータセットを使って結果の妥当性を評価する
* 問題なければプロダクトの機能として実装を進める
  * 一旦実験系のIssueだけ立てておき、機能することがわかった段階でプロダクトへの実装イシューを立てる

**コメント:**

- **nishio** (2025-03-25T16:25:22Z):

(1.)の関連
[Talk to the City Turboのプロンプト](https://scrapbox.io/nishio/Talk_to_the_City_Turbo%E3%81%AE%E3%83%97%E3%83%AD%E3%83%B3%E3%83%97%E3%83%88)

---

### [[DOCUMENT] Azure である程度の期間運用する際に必要な項目を追加する](https://github.com/digitaldemocracy2030/kouchou-ai/issues/175)

**作成者:** shingo-ohki  
**作成日:** 2025-03-25T08:21:14Z  
**内容:**

# 現在の問題点
- 最初に構築するときのことしかケアできていない
- 何らかの理由(環境変数を更新した、新機能が使いたくてコードを更新した、ロゴを設定した、など)でコンテナを作り直すときにはまりどころがある

> フルでmakeしちゃうと新しいACRが作られちゃうのか？→.env.azure.generatedに書き出されたACR名を.env.azureに転記していなかったので毎回生成されていた
from https://w1740803485-clv347541.slack.com/archives/C08F7JZPD63/p1742889861058199?thread_ts=1742886821.947769&cid=C08F7JZPD63

> コンテナを再起動して生成済みレポートが消える
> ソースコードが更新されて新機能が追加されたらみんな新機能を使いたくて作り直しをすると思いますけど、それでレポートが全部消えてたら泣かれるかもw
> 分析して「よし静的HTMLを生成して公開しよう、そのためにはロゴを入れて更新」で分析結果が消える
from https://w1740803485-clv347541.slack.com/archives/C08F7JZPD63/p1742889178309719

# 提案内容

> 環境変数を変更したい時とか、ソースコードをupdateしたい時のためのマニュアルがあればいい

**コメント:**

- **nishio** (2025-03-25T08:26:40Z):

移動しなくても概要がわかるようにチャットを引用しときました

- **nishio** (2025-03-25T08:28:16Z):

関連 [FEATURE]ストレージ連携 · Issue #46 


- **nasuka** (2025-03-25T14:01:33Z):

> コンテナを再起動して生成済みレポートが消える

ここだけはなるはやで追記した方が良いと思うので、この後私の方で追記しますね。
-> done
https://github.com/digitaldemocracy2030/kouchou-ai/pull/181

---

### [[FEATURE] 生成するレポートを永続化できるようにする](https://github.com/digitaldemocracy2030/kouchou-ai/issues/174)

**作成者:** shingo-ohki  
**作成日:** 2025-03-25T08:17:16Z  
**内容:**

# 背景
（特に Azure 環境では）コンテナをつくり直すとそれまでに生成したレポートが消えてしまう
https://w1740803485-clv347541.slack.com/archives/C08F7JZPD63/p1742889178309719

# 提案内容
例えば、
1. レポート生成時に永続化できるようにする（Azure のストレージサービスや Google drive など?） 

**コメント:**

- **nasuka** (2025-03-25T08:20:56Z):

起票いただきありがとうございます！
類似のIssueがあるのでこちらに貼っておきます。
https://github.com/digitaldemocracy2030/kouchou-ai/issues/46

---

### [[FEATURE]グラウンディングの実験](https://github.com/digitaldemocracy2030/kouchou-ai/issues/173)

**作成者:** nasuka  
**作成日:** 2025-03-25T08:10:43Z  
**内容:**

# 背景
https://github.com/digitaldemocracy2030/kouchou-ai/issues/172
* 上記のイシューに記載しているグラウンディングの実験を行う


# 実施内容
以下を実施する想定

* グラウンディング処理を行う実験スクリプトを実装
* 検証データに対してグラウンディングされたクラスタ説明文を出力
* 結果を確認し、問題なければプロダクトの機能として実装する
  * 確認のプロセスについては要検討

**コメント:** なし

---

### [[FEATURE]クラスタ説明文におけるグラウンディングの実装](https://github.com/digitaldemocracy2030/kouchou-ai/issues/172)

**作成者:** nasuka  
**作成日:** 2025-03-25T08:07:39Z  
**内容:**

# 背景
* クラスタの説明文では所属する意見の内容を解説しているが、本当にそのような意見が存在するのか確認するのに手間がかかる
* レポートの説得力を増す上で、説明の根拠となる元データを簡単に参照できるようにしたい


# 提案内容
* クラスタ説明文において、その根拠となるargumentを紐づけたテキストを表示する
  *  参考: https://medium.com/jigsaw/making-sense-of-large-scale-online-conversations-b153340bda55
    * Groundings
    * 紐づけ方・紐づけた文章の生成のさせ方は様々なアプローチがあるので、アプローチを検討する部分からassigneeの方にお任せする

# 進め方について
* いきなり機能を実装するのではなく、プロダクトとは独立して実験スクリプトを実装し、検証用のデータセットを使って結果の妥当性を評価する
  * 問題なければプロダクトの機能として実装を進める
  * 一旦実験系のIssueだけ立てておき、機能することがわかった段階でプロダクトへの実装イシューを立てる



**コメント:** なし

---

### [[FEATURE]ファクトチェック機能の実装](https://github.com/digitaldemocracy2030/kouchou-ai/issues/170)

**作成者:** nasuka  
**作成日:** 2025-03-25T06:18:39Z  
**内容:**

# 背景
* 入力ファイル内のコメントが虚偽の場合がある
  * e.g. 「◯◯という人物が✗✗という発言をしていたが大変嘆かわしい」というコメントがあったとして、現状ではこのコメントの真偽に関わらずコメントが分析結果に組み込まれてしまう

# 提案内容
* 個別のコメント（or 意見）についてファクトチェックを行う
* クラスタリングやクラスタ説明文の生成時にファクトチェックの結果を組み込み
  * 組み込む方法はいくつかパターンがありそう
    * 1. 虚偽と判定されたargumentはクラスタ生成以降のプロセスで除外する
    * 2. クラスタタイトルや説明文生成時に、argumentのテキストだけでなくファクトチェックの結果（真偽）も入力して生成を行う
    * 3. 散布図上でargumentをホバー表示する際に、虚偽の疑いがあるargumentはそのことが分かるように表示を変える
  * ↑は一例だが、実現方針の具体化からassigneeの方にやっていただけるとありがたい

# 進め方
* いきなり機能を実装するのではなく、プロダクトとは独立してスクリプトを実装し、検証用のデータセットを使って結果の妥当性を評価する
  * 問題なければプロダクトの機能として実装を進める
  * 一旦実験系のIssueだけ立てておき、実験結果より自動評価が機能することがわかった段階でプロダクトへの実装イシューを立てる



**コメント:** なし

---

### [[FEATURE]dependabotの導入](https://github.com/digitaldemocracy2030/kouchou-ai/issues/151)

**作成者:** nasuka  
**作成日:** 2025-03-25T05:54:10Z  
**内容:**

# 背景
* セキュリティの脆弱性に伴うパッケージのアップデートを行いたい
* 現状でもgithub上の `Security` でアラートはくるが、パッケージアップデートをする際は手作業が入る


# 提案内容
* dependabotを用いてパッケージアップデートのPR作成を自動化する

**コメント:** なし

---

### [[FEATURE]API呼び出し前にCSVファイル内の意見数を確認する](https://github.com/digitaldemocracy2030/kouchou-ai/issues/147)

**作成者:** ei-blue  
**作成日:** 2025-03-25T05:27:30Z  
**内容:**

# 背景
CSVファイルのデータから最終的に抽出された意見の数が詳細設定で設定されたクラスタ数を下回っていると、クラスタリングの過程でエラーになり、無駄にAPIを呼び出すことになってしまう。

# 提案内容
「レポート作成を開始」ボタンを押した際にクラスタ設定の数とCSVファイルの行数を比較し、CSVファイルの行数の方が少ない場合に警告を出す。
コメント数（CSVファイルの行数）＝最終的な意見の数　ではないため、エラーにする必要はない。

**コメント:**

- **ei-blue** (2025-03-25T05:27:39Z):

/assign

---

### [[FEATURE]LLMによるクラスタ品質の自動評価（実験）](https://github.com/digitaldemocracy2030/kouchou-ai/issues/144)

**作成者:** nasuka  
**作成日:** 2025-03-25T03:36:54Z  
**内容:**

# 背景
https://github.com/digitaldemocracy2030/kouchou-ai/issues/143

* こちらのイシューは上記のサブイシュー


# 提案内容
* LLMによるクラスタ品質の自動評価の実験を行う
  * 出力されたクラスタタイトル・説明文・所属データ点の情報に基づいて、LLMでクラスタの品質を評価する
* どのようなアプローチで評価するかは、assigneeの方におまかせする
  * 例としては、例えば以下のような評価項目のスコアをLLMで出力するようなアプローチがある
    * クラスタ内部の一貫性評価
      * クラスタタイトル・説明文・所属データのテキストを入力し、一貫性を100点満点でスコアリングする
    * クラスタ外部との分離度の評価
      * クラスタAの情報（タイトルや所属データ等）と、重心の距離が最もAに近いクラスタBの情報をLLMに入力し、分離度を出力する


**コメント:** なし

---

### [[FEATURE]クラスタ品質の自動評価](https://github.com/digitaldemocracy2030/kouchou-ai/issues/143)

**作成者:** nasuka  
**作成日:** 2025-03-25T03:35:01Z  
**内容:**

# 背景
* クラスタリング結果が妥当なものになっているのかを検証したい
* 一方で、個別のクラスタを人手で評価するのは非常に労力がかかる
  * 50件のクラスタについて整合性を確認することは難しい

# 提案内容
* クラスタリングの結果について自動評価を行う
  * アプローチの詳細は個別のサブイシューに記載する

# 進め方について
* いきなり機能を実装するのではなく、プロダクトとは独立して評価スクリプトを実装し、検証用のデータセットを使って評価実験を行う
* 自動評価の結果について妥当性を確認し、問題なければプロダクトの機能として実装を進める
  * 一旦実験系のIssueだけ立てておき、実験結果より自動評価が機能することがわかった段階でプロダクトへの実装イシューを立てる


## 対象データセット
* 文化庁のパブリックコメントのデータセットが使える
  * https://www.bunka.go.jp/seisaku/bunkashingikai/chosakuken/hoseido/r05_07/
* 現在開示請求しているエネルギー庁のパブコメのデータも使える可能性がある



**コメント:** なし

---

### [[BUG] Unknown event handler property `onFileRemove`. が出る](https://github.com/digitaldemocracy2030/kouchou-ai/issues/142)

**作成者:** shingo-ohki  
**作成日:** 2025-03-25T03:25:55Z  
**内容:**

### 概要

https://github.com/digitaldemocracy2030/kouchou-ai/commit/685bb7c685e281ad3afb760bc8e7c9d649532d41

の状態のコードで localhost:4000/create にアクセスすると以下のエラーが出る。

`Unknown event handler property `onFileRemove`. It will be ignored.
`
### 再現手順

1. https://github.com/digitaldemocracy2030/kouchou-ai/commit/685bb7c685e281ad3afb760bc8e7c9d649532d41 を checkout
2. docker compose up
3. ブラウザで localhost:4000/create にアクセス

### 期待する動作
エラーが出ないこと

### スクリーンショット・ログ

![Image](https://github.com/user-attachments/assets/71256468-62ea-40fe-aa58-ccfbbe88199f)

![Image](https://github.com/user-attachments/assets/55429512-79dc-4dd6-8bbe-a6d0b5ee98a0)

### その他

<!-- 追加で伝えておきたいことがあれば記入してください -->

**コメント:**

- **shingo-ohki** (2025-03-25T03:26:58Z):

/assign

---

### [[FEATURE] OGPカードを魅力的なものにする](https://github.com/digitaldemocracy2030/kouchou-ai/issues/140)

**作成者:** takahiroanno  
**作成日:** 2025-03-25T02:49:25Z  
**内容:**

# 背景
SNSなどでシェアされることによって広聴AIの存在が広く知られる

# 提案内容
<!-- 実装案やデザイン案があれば記入してください -->

**コメント:**

- **shgtkshruch** (2025-03-25T15:07:08Z):

![Image](https://github.com/user-attachments/assets/cdea6b27-7618-421f-ab9f-4ca9621c88a3)

Next.js に OGP 画像を生成する機能があるので、試しにレポートの個別ページのデータで OGP 画像を作ってみました。
https://nextjs.org/docs/app/api-reference/file-conventions/metadata/opengraph-image
（実際に利用するにはデプロイする環境周りの調査も必要そう）

タイトルとサイト名に加えて、議論のボリューム感がザックリと掴めるかなと思ったのでページ下部の Analysis のデータものせてみました。
デザイナーさんのデザインが欲しいですね... 💄 

元にしたページの表示
![Image](https://github.com/user-attachments/assets/2c54eff5-c50f-47e4-9680-52f0275136b4)

![Image](https://github.com/user-attachments/assets/284e20ad-6091-4d39-951f-7c361cb06685)

- **nishio** (2025-03-25T15:13:08Z):

いまのOGPがひどすぎるのでとりあえずこれでGOしちゃっていいのではと思いました

https://github.com/digitaldemocracy2030/kouchou-ai/issues/114
これは変えてもいいかもです

---

### [テスト](https://github.com/digitaldemocracy2030/kouchou-ai/issues/135)

**作成者:** nasuka  
**作成日:** 2025-03-23T02:33:21Z  
**内容:**

## 要望内容
テスト

---
こちらのイシューはGoogle Form経由で投稿されたものです

**コメント:** なし

---

### [テスト用イシューです](https://github.com/digitaldemocracy2030/kouchou-ai/issues/134)

**作成者:** nasuka  
**作成日:** 2025-03-23T02:33:18Z  
**内容:**

## 要望内容
テスト

---
こちらのイシューはGoogle Form経由で投稿されたものです

**コメント:** なし

---

### [[DOCUMENT]Azureのセットアップガイドに関する免責事項を記載する](https://github.com/digitaldemocracy2030/kouchou-ai/issues/133)

**作成者:** nasuka  
**作成日:** 2025-03-23T02:11:50Z  
**内容:**

# 現在の問題点
- セットアップ手順に従った結果に対する責任範囲が明確に定義されていない
  - 利用者がトラブル発生時にプロジェクトに過度な責任を求める可能性がある

# 提案内容
以下のような免責事項を記載する

* 本ドキュメントは情報提供のみを目的としており、特定の環境でのデプロイを保証するものではありません。
* 本ガイドに従って実施されたデプロイや設定によって生じた問題、損害、セキュリティインシデントについて、作者および関連プロジェクト貢献者は一切の責任を負いません。
* 各組織のセキュリティポリシーやコンプライアンス要件に従って適切に評価・カスタマイズしてください。


**コメント:**

- **nasuka** (2025-03-23T02:13:42Z):

https://github.com/digitaldemocracy2030/kouchou-ai/pull/115
のmerge後に対応する

---

### [[FEATURE] 意見データの入力にGoogle スプレッドシートのデータを使えるようにする](https://github.com/digitaldemocracy2030/kouchou-ai/issues/132)

**作成者:** shingo-ohki  
**作成日:** 2025-03-23T01:31:08Z  
**内容:**

# 背景
- #124 とは別のルートとして、意見データとしてGoogle スプレッドシートのデータが使えると文字コードの問題を回避できる
- #105 のパブコメ自体を Google Form で集めるように標準化できると、それをそのまま広聴AIに流し込める

# 提案内容
Google スプレッドシートのURLを指定できるようにする

- [x] #182 
- [ ] 非公開のSpreadsheetにサービスアカウントをinviteしてもらってそれを読む

**コメント:**

- **takahiroanno** (2025-03-25T01:40:28Z):

確かに、Google Form -> Google Spreadsheet -> 広聴AIのコンボはわかりやすいですね

- **nishio** (2025-03-25T03:25:24Z):

(SlackLogExporterの方のニーズで)Google Spreadsheet APIとGoogle Drive APIはenagleにして、サービスアカウントも作りました。

- 公開のSpreadsheetを読む
- 非公開のSpreadsheetにサービスアカウントをinviteしてもらってそれを読む

の2通りの経路があると思います。

- **shingo-ohki** (2025-03-25T14:40:25Z):

/assign

- **shingo-ohki** (2025-03-26T10:50:58Z):

> 公開のSpreadsheetを読む

こっちは #182 で完了

- **shingo-ohki** (2025-03-28T05:35:40Z):

> 非公開のSpreadsheetにサービスアカウントをinviteしてもらってそれを読む

この機能は、あるとよいとは思うものの現段階でやっておいた方がよいのかどうか迷っています。
もやもやしているのは以下

- 現在、生成されたレポート（出力結果）にはアクセス制限がないので、この状態でアクセス制限のかかった入力データを扱えるようにするのはどれくらい意味があるか？（そういうニーズがある？）

- このツールの利用者が、ローカル環境や Azure でこのツールを動かしてレポート生成を行う使い方では、アクセス制限されたスプレッドシートを読み取れるようにするユースケースが思い当たらない。（サービスアカウントを発行して設定するという新たな手間が発生する）一方で、SaaS として提供するなら必要性はあるのかも。

- **shingo-ohki** (2025-03-28T05:37:18Z):

いったん /unassign 

- **shingo-ohki** (2025-03-28T05:37:52Z):

/unassign

---

### [[DOCUMENT]ソースコードの実装以外での貢献方法がもっと言語化されるとよい](https://github.com/digitaldemocracy2030/kouchou-ai/issues/130)

**作成者:** nishio  
**作成日:** 2025-03-22T14:31:29Z  
**内容:**

# 現在の問題点
非エンジニアが何をしたらいいかわからない

# 提案内容

例えば
- GitHubのissuesをみて「その問題が解決されると自分も助かる！」と思ったものに:+1:をつけるのはタスクの優先付の参考になるので貢献
- 質問をするのは言語化のきっかけになるので貢献
- 将来的に「AのレポートとBのレポートのどっちがいいですか？」をやる可能性がある、そう言うのに回答してくれるのは貢献

他に思いついたら下にコメントつけてください

**コメント:**

- **shingo-ohki** (2025-03-22T15:14:32Z):

- 思っていることをどこかに発言するだけで貢献
  - 投稿があるSlackチャンネルは盛り上がる、議論のきっかけになる
  - 他の人がどう思っているかが分かる
  - 口火をきると他の人が発言しやすくなる
- これっていいなと思ったことにスタンプで反応するだけでも貢献
- エンジニアはどうしても作り手側の視点になりがちなので、非エンジニアの率直な感想はユーザー目線に近く、思っているより貴重（「何でかは分からないけど、ここ分かりにくい」というのは分かりにくさの言語化のきっかけになる）
- 使ってみて、ここがこう便利だった、こう使ってみたらこうなったというのも相当有益（うまくいかなくてもそれ自体が有益）
- こんなこと書いても大丈夫かな？は悪意がなければ大抵大丈夫
- 自主的に動いたり、発言したりしている人にとっては反応があるだけでも嬉しい

- **naoyo4** (2025-03-23T00:10:33Z):

以下、非エンジニアだけど、**元エンジニア：隠居中**でもある自身の目標

＊非エンジニアが疎外感を持ちにくいよう、エンジニアとの間の**橋渡し**
　・自分も理解していないけど、何となく概念的にはこんな感じかなって素朴な質問をする
　（ただし、なるべくポイントは外さないように・・・）

＊ユーザーはいても、テスターがいないので、なるべく**テスター的立ち位置**をとる
（基本、品質管理部門等は、製造部門からは嫌われがちがけど、重要なお仕事）
　・根本的に中身を理解してない（できない）けど、ブラックボックス・テスト的なものは可能？
　（適切なテストデータ作成と結果検証ができるかといえば、正直難しいけど、少なくとも自身の理解は深まる）

＊「悪魔の代弁者」的、「**キュートな小悪魔**」を目指す。以下、その役割
　・意見に対する盲目的な賛成を防ぐ﻿
　・問題点やリスクを浮き彫りにする﻿
　・検討の幅を広げて、より客観的でバランスの取れた判断を促す﻿
　・集団思考を防ぎ、創造性を刺激する﻿
　・潜在的な問題を特定し、リスクを軽減する﻿
（まあ、これもきちんとした理解がない限り、嫌われるだけなので、マイルドでキュートな方法で）

まあ、気持ちだけ置いておこう。



- **shingo-ohki** (2025-03-23T00:38:07Z):

- オンボーディングプロセスへの貢献
  - 参加して疑問に思ったことを聞く
    - やり取りされている質問と回答をFAQにまとめる（ドキュメントに反映する）
  - 何が分からないのかを書く
- ユースケース探索への貢献
  - こんなことに使えるんじゃないか？というのを書いてみる、やってみる
- 話していることを他の人が理解しやすいようにまとめてみる（LLMに投げた結果を貼る）

- **shingo-ohki** (2025-03-23T00:41:36Z):

簡単なやつがありました
- 自己紹介を `#02_introduction` チャンネルに書く
  - どういう人が参加している人が分かる
  - こういう人がいるならこういうことができるんじゃないかというアイディアがでる

- **nasuka** (2025-03-23T01:19:46Z):

* 広聴AIで試してみたい/試したら面白そうなデータセットを共有する
* コミュニティに参加してみた感想や広聴AIのレポートに関する感想等をブログ/SNSなどで発信する
  * プロジェクトに対してより多くの人に興味を持っていただく上で意義があると思っています
  * ほづみさんの例: https://x.com/ninofku/status/1903017097586004251
    * ほづみさんの例はツールを使ってみた感想なので多少エンジニアリング知識が必要ですが、「レポートを見た感想」「コミュニティに参加してみて感じたこと」などは、ノンエンジニアの方でも発信できる & 発信する意義があると思います

- **mami-st** (2025-03-23T01:56:43Z):

非エンジニアです。
雑ですが、ちょうど今朝o1 pro に相談してた内容と重なるところがあったのでご参考までにシェアさせてください！

<img width="706" alt="Image" src="https://github.com/user-attachments/assets/5ae3eefb-0682-4982-a53a-baea6119bdea" />

<img width="680" alt="Image" src="https://github.com/user-attachments/assets/97a5054b-6d2b-4dcb-ae0f-f9e176279a04" />

<img width="699" alt="Image" src="https://github.com/user-attachments/assets/5485c526-a68a-4916-883c-fc573c3d0ad3" />

[📘ChatGPT-非エンジニアの文系プロダクトマネージャーがOpenAIのDeepResearchを使って、特定のGitHubのリポジトリから情報を得るベストプラクティスが知りたいです。まずは、得られる情報の種類を網羅的に解説してください。.md](https://github.com/user-attachments/files/19406582/ChatGPT-.OpenAI.DeepResearch.GitHub.md)

- **nishio** (2025-03-23T02:26:52Z):

(issueを開いてみたはいいものの着地の仕方を考えてなかった！)

- **nishio** (2025-03-24T01:47:45Z):

ランディングページ的な物が整備されつつあるので多分そこに合流するのが良さそう

---

### [[FEATURE] OpenRouterを用いて動くようにする](https://github.com/digitaldemocracy2030/kouchou-ai/issues/128)

**作成者:** 101ta28  
**作成日:** 2025-03-22T14:07:01Z  
**内容:**

# 背景
[idobata-analyst](https://github.com/digitaldemocracy2030/idobata-analyst) では、AI呼び出しに[OpenRouter](https://openrouter.ai)を用いている。

環境構築時に共通プラットフォームのKeyを用いることができれば便利だと思うため。

また、(OpenAI以外の)複数モデルの切り替えがしやすいものが良いと思ったため。

# 提案内容

server ディレクトリ内の`config.py`や`hierarchical_utils.py`を変更すれば動くと思われます。

**コメント:**

- **nishio** (2025-03-22T14:13:11Z):

embeddingとextractionからの呼び出しはservice/llm.pyに集約されつつあって、そこで環境変数を読んでAzure OpenAI Serviceと切り替えているので、そこにOpenRouterも追加すると言うのは手だと思います

- **101ta28** (2025-03-22T14:38:07Z):

/assign

- **101ta28** (2025-03-22T16:54:28Z):

悲しいかな OpenRouter は embedding 非対応なので、そこは OpenAI or Azure 頼みですね...

issue立てましたが、どっちみちOpenAIに頼ってしまう形になるので、closeしたほうが良いかもしれないです。

OpenRouterがembedding対応したら変更とかで良さそう...

- **nishio** (2025-03-22T17:27:30Z):

なるほど、じゃあ一旦wontfixにしてみます

- **blu3mo** (2025-03-23T06:16:56Z):

文脈を補完しておくと、いどばたでOpenRouterを使い始めた一番の理由は「Google Gemini APIだとrate limitを上げるのが面倒だが、Open Routerはお金さえ入れればrate limitを上げられるから」です

---

### [[FEATURE]Shift-JISのcsvをUTF-8に変更する](https://github.com/digitaldemocracy2030/kouchou-ai/issues/124)

**作成者:** yuneko1127  
**作成日:** 2025-03-22T04:56:29Z  
**内容:**

# 背景
<!-- なぜその機能が必要なのか、何が改善されるのか具体的に記入してください -->
ExcelなどでCSVを作成するとShift-JISになり、非エンジニアの利用を考えるのであれば、文字コードの変換は利用者側ではなくシステム側でやるべきだと考えるから。


# 提案内容
<!-- 実装案やデザイン案があれば記入してください -->
最初にcsvを読んでいるところで、UTF-8でない場合は別の処理をする。

**コメント:**

- **yuneko1127** (2025-03-22T04:57:14Z):

/assign

---

### [[FEATURE]文字コードがSJISやBOMがついてるときPythonで変換する](https://github.com/digitaldemocracy2030/kouchou-ai/issues/123)

**作成者:** nishio  
**作成日:** 2025-03-22T04:50:42Z  
**内容:**

# 背景
ExcelからCSVを書き出す時、だいたいSJISで書き出してしまうしUTF-8にするとしてもBOMをつけてしまったりする

# 提案内容
エラーにするより、しれっと変換したほうが説明コスト低いのではないか


**コメント:**

- **nishio** (2025-03-22T08:09:22Z):

duplicate

---

## 過去1週間に更新されたissue（作成・クローズを除く）(28件)

### [[FEATURE] コード以外の貢献も可視化する](https://github.com/digitaldemocracy2030/kouchou-ai/issues/122)

**作成者:** shingo-ohki  
**作成日:** 2025-03-21T22:56:37Z  
**内容:**

プロジェクト固有の話題ではないですが、一旦こちらに

# 背景

現在、GitHub リポジトリへのコードのマージのみがコントリビューションとして可視化されています。しかし、プロジェクトの進行には以下のようなコード以外の重要な貢献もあります。

- Slack やオンラインミーティングでの議論・調整
- PR や Issue に対するレビューコメント・フィードバック
- #デジタル民主主義2030 のハッシュタグをつけた Twitter（X）での発信
- その他、プロジェクトの前進に貢献する活動

これらの貢献も適切に可視化することで、より多くの人が参加しやすくなり、
現在の「手が足りない」問題の解消や「属人化をなくす」ことにつながるのではないかと考えました。

# 提案内容

コード以外の貢献を記録・可視化する仕組みを検討するのはどうでしょうか？ 例えば、以下のような方法が考えられます。

- Slack や Twitter（X）での貢献を記録する仕組み（例: GitHub Actions で定期的に収集）
- コントリビューションログを作成し、定期的にレポートを公開

また、「プロジェクト本体のコードには手を出しづらいけど、このような形なら参加しやすい」という人が貢献しやすくなるという効果も期待できます。

参考: https://chatgpt.com/share/67ddda49-b6b8-800c-96c3-0a02a62b8839

また、いどばた の仕組みを一部流用できる可能性も考えられ、
熟議への参加や政策提案・法案成立へのコントリビューション可視化にもつながるかもしれません。

**コメント:**

- **nishio** (2025-03-22T08:11:45Z):

Tobanを使うと言う案
https://note.com/takerunakao/n/nb32a8fc1d557

---

### [[BUG]縦長画面での散布図の表示がおかしい](https://github.com/digitaldemocracy2030/kouchou-ai/issues/121)

**作成者:** nishio  
**作成日:** 2025-03-21T15:32:58Z  
**内容:**

### 概要

<img width="453" alt="Image" src="https://github.com/user-attachments/assets/c20dbff2-454c-4b23-bf8b-973bcc6c96fd" />


横長の時の表示:
<img width="1512" alt="Image" src="https://github.com/user-attachments/assets/1b7a062a-5413-4d24-b5f3-91cb81059d07" />

<!-- バグの簡潔な説明をお願いします -->

### 再現手順

1. 縦長画面で見る

### 期待する動作

- 理論的な理想を言うと、そもそもアスペクト比は1:1であるべき
- 一方でそれにこだわって徹底した場合にみやすさが損なわれるのも問題がある
- 縦長画面で見た場合はラベルの幅との干渉でアスペクト比が大きく狂っているのでそこだけでも直すか？

### スクリーンショット・ログ

<!-- 必要に応じてスクリーンショットやエラーログなどを添付してください -->

### その他

<!-- 追加で伝えておきたいことがあれば記入してください -->

**コメント:** なし

---

### [[FEATURE]「どのフィールドをcommentとするか」を指定できる機能](https://github.com/digitaldemocracy2030/kouchou-ai/issues/116)

**作成者:** nishio  
**作成日:** 2025-03-21T05:24:46Z  
**内容:**

# 背景
Shutaro Aoyama (ぶるーも)
昨日こうちょうAIを試して、csvフォーマットが絶妙に違うのがだるいなと思いました（ここはコミュニケーションとった方がよかったですね、、）
いどばたcsvのcontentをcommentに変えるとこうちょうAIに突っ込めるという認識


NISHIO Hirokazu
現状はまずはノンエンジニアが使えるようにWebUIを頑張ってますけど、将来的にはAPIでレポート生成をトリガーできるべきで、その時に「どのフィールドをcommentとするか」を指定できるのが理想だと思います 

# 提案内容

defaultが"comment"であるような"target-column"属性を受け取るようにし、そのカラムを分析対象とする。
アンケートのようなデータソースでは通常複数のカラムがあるので、個別にCSVを保存し直さなくても分析できるようになって楽。

**コメント:** なし

---

### [[REFACTOR] 濃いクラスタのアイコン変更](https://github.com/digitaldemocracy2030/kouchou-ai/issues/113)

**作成者:** nishio  
**作成日:** 2025-03-20T12:20:30Z  
**内容:**

# 現在の問題点

<img width="249" alt="Image" src="https://github.com/user-attachments/assets/bc626d04-e7c0-4245-9b01-e762d433a434" />

濃いクラスタのアイコンは特に意味はなくこれになっている


# 提案内容

多分叩き台の案がないとどう変えたらいいかの議論もできないと思うので雑に描いておく

![Image](https://github.com/user-attachments/assets/9e46dfd6-71d4-4c2b-bbd5-1c79220c8d80)

アイコンとしてデザインできるかは度外視して描くとこんな感じで「全体像」は全体にたくさんの点が散らばっており、「濃いクラスタ」はぎゅっとした「濃い」「密度の高い」塊がいくつかある感じ

**コメント:** なし

---

### [[FEATURE]クラスタ見出しをanchorにする](https://github.com/digitaldemocracy2030/kouchou-ai/issues/112)

**作成者:** nishio  
**作成日:** 2025-03-20T12:12:16Z  
**内容:**

# 背景

<img width="832" alt="Image" src="https://github.com/user-attachments/assets/4f696633-40b9-47c4-924d-01ab50c0c50c" />

# 提案内容

展開表示するものは将来的には階層クラスタリングのデータから取れるかもしれないが、とりあえずanchorにしたら特定の見出しにリンクして言及できるようになって良いのではないか

**コメント:** なし

---

### [[FEATURE]用語解説ページをつける](https://github.com/digitaldemocracy2030/kouchou-ai/issues/111)

**作成者:** nishio  
**作成日:** 2025-03-20T12:07:35Z  
**内容:**

# 背景
「プロンプト」「埋め込み」「濃い(クラスタ)」について、単語レベルで言い換えてもわかりやすくならない気がするので、やるとしたら用語解説ページをつけるとかかな

「縦軸・横軸はなんだろう」についても解説

# 提案内容
<!-- 実装案やデザイン案があれば記入してください -->

**コメント:**

- **nishio** (2025-03-21T07:24:10Z):

# 広聴AI 用語解説

## プロンプト

プロンプトとは、AIモデル（大規模言語モデル）に対して与える指示文のことです。広聴AIでは、コメントから意見を抽出したり、クラスタにラベルを付けたりする際に、AIに対して特定の形式で回答するよう指示するために使用されています。

プロンプトは、AIが実行すべきタスクの内容、期待される出力形式、考慮すべき制約条件などを含み、AIの出力品質を大きく左右する重要な要素です。広聴AIの各処理ステップ（抽出、初期ラベリング、統合ラベリング、要約など）のために、それぞれ専用のプロンプトが用意されています。レポートの質を良くするために修正することも可能で、レポート作成者がどのようなプロンプトを使ったかは生成されたレポートの末尾で見ることができます。

## 埋め込み（ベクトル表現）

埋め込みとは、テキストデータを数値のベクトル（多次元の数値の配列）に変換したものです。広聴AIでは、抽出された意見（議論）の内容を数学的に処理できる形式に変換するために使用されています。

この変換により、意味的に似ている文章がベクトル空間上で近い位置に配置され、プログラムがテキストの意味的な類似性を計算できるようになります。広聴AIでは、この埋め込みベクトルを基にして、類似した意見をグループ化（クラスタリング）する処理が行われています。

## 濃い（クラスタ）

「濃いクラスタ」とは、広聴AIにおいて特に密度の高い（多くの類似した意見が集まっている）クラスタを指します。クラスタの「濃さ」は、そのクラスタ内の意見の密度によって決まります。

広聴AIでは、大量の意見の中から特に注目すべき意見グループを見つけやすくするために、「濃いクラスタ設定」機能が提供されています。この機能を使うと、密度の高いクラスタのみをフィルタリングして表示することができ、重要な意見グループに焦点を当てた分析が可能になります。

## 縦軸・横軸

広聴AIの散布図表示における縦軸と横軸は、意見の埋め込みベクトルを2次元に圧縮して表示したものです。多次元の埋め込みベクトルを視覚化するために、次元削減技術が使用されています。

この2次元平面上では、意味的に類似した意見は互いに近い位置に配置されます。つまり、チャート上で近くに表示されている意見は内容が似ていて、遠くに表示されている意見は内容が異なる傾向があります。縦軸と横軸自体には特定の意味はなく、あくまで多次元データを2次元で表現するための座標軸です。

---

### [[FEATURE]パブコメ形式でレポート出力するようにする](https://github.com/digitaldemocracy2030/kouchou-ai/issues/105)

**作成者:** takahiroanno  
**作成日:** 2025-03-20T07:47:45Z  
**内容:**

# 背景
具体的なユースケースとして、行政機関においてパブコメを分析することがありそう。
その際に、よく用いられている方式で意見のカタマリをexportできると、自治体のユーザーにとって使いやすくなる。

例
- https://www.mlit.go.jp/common/001034196.pdf
- https://www8.cao.go.jp/cstp/pubcomme/kihon4_toshin/kekka2.pdf

# 提案内容

- レポート出力、ボタンをおく（チャートの右上に並べるのが一案か）
- ３カラムでcsvを出力する
  - 大分類
  - 小分類（濃いクラスタのみ）

**コメント:**

- **ei-blue** (2025-03-21T06:56:26Z):

/assign


---

### [[FEATURE] ツールの利用状況を知る仕組み](https://github.com/digitaldemocracy2030/kouchou-ai/issues/104)

**作成者:** shingo-ohki  
**作成日:** 2025-03-20T07:42:15Z  
**内容:**

# 背景
このツールが様々なところで使われるようになった際に、現状想定している利用方法（各利用者がツールの環境を作って利用する）の場合、このツールの実際の利用状況を知る手段が少ない


# 提案内容
例えば、あらかじめドキュメントなどで説明した上で、レポート生成を行うたびに Google Analytics が設定された特定のURLにリクエスト（生成するレポートについての情報は含まない、ツールを使ったということが分かる情報のみ）を飛ばすようにしておくと、そのアクセス解析を行うことで、いつどこでレポート生成が行われたかを知ることができ、このツールの利用状況が得られるようになり、その情報を広報活動や開発に活用できる

というのはどうでしょうか？

**コメント:** なし

---

### [[FEATURE]CSVのフォーマットのエラーをわかりやすくする](https://github.com/digitaldemocracy2030/kouchou-ai/issues/97)

**作成者:** nishio  
**作成日:** 2025-03-19T02:43:19Z  
**内容:**

# 背景
>従来のフォーマット(comment-body)の物をいれると画面遷移せずにトースターでエラーが表示されるがエラーの詳細はないので解決方法が分からなさそう、ここはカラム名の間違い、文字コードがSJIS、BOMがついてる、などなどいろんなハマりバターンが予想されるのでケアできると良さそう


# 提案内容
<!-- 実装案やデザイン案があれば記入してください -->

**コメント:**

- **nishio** (2025-03-22T12:34:44Z):

エラーメッセージを出すよりも、システム側で変換できるものは変換した方が良いという議論 #124

---

### [[FEATURE]50件の小さいデータで試した場合に濃いクラスタ抽出で見た目が変わらない問題の解決](https://github.com/digitaldemocracy2030/kouchou-ai/issues/96)

**作成者:** nishio  
**作成日:** 2025-03-19T02:41:35Z  
**内容:**

# 背景
50件の小さいデータで試した場合に濃いクラスタ抽出で見た目が変わらないことに混乱する


# 提案内容

案1:

>濃いクラスタ抽出で見た目が変わらないのはデータが少なすぎて実行されてないからか？そういう時にはボタンを非表示にしたいかも。クリックして変わらないのは混乱させる

この方法が良いかはわからない

**コメント:**

- **takahiroanno** (2025-03-20T07:41:37Z):

これ確かに気になりました！

- **nasuka** (2025-03-23T01:55:59Z):

まず、見た目が変わらないのは想定した挙動ではないですね 😢 
（クラスタ数・データ数の条件にもよりますが）件数が少ない場合は何も表示されないのが想定している挙動で、今は全体図と同じ図がそのまま表示されておりこちらは想定外の挙動になります。

そもそも濃いクラスタ抽出は2層目のクラスタ数と比較してある程度データの件数がないとワークしないので、
クラスタ数:データの件数の比率が一定以下の場合は濃いクラスタ自体を非表示にした方が良いかもしれません。
レポート作成時、非表示になる場合はしきい値を下回っているので濃いクラスタが抽出できない旨をフロント側でアラートしてあげると良さそう。

- **nishio** (2025-03-26T15:30:02Z):

デザイン的にはボタンがdisabledになって、ホバーで「データが少ないので利用できません」と出すイメージです

- **nasuka** (2025-03-27T08:30:01Z):

> デザイン的にはボタンがdisabledになって、ホバーで「データが少ないので利用できません」と出すイメージです

ありがとうございます、自分としては違和感ないです！

---

### [[REFACTOR] フロントエンドのコードを prettier でフォーマットをする](https://github.com/digitaldemocracy2030/kouchou-ai/issues/84)

**作成者:** shgtkshruch  
**作成日:** 2025-03-18T03:59:30Z  
**内容:**

# 現在の問題点
<!-- 現在のコードの何が問題なのか、どのような技術的負債があるかを説明してください -->

- この issue のスコープとしては、フロントエンドに関わる client, client-admin, utils/dummy-server を想定しています
- コードの formatter が導入されていないため、開発者によってコードの書き方（ex. 改行、スペースの入れ方）に差分出てくる可能性がある

# 提案内容
<!-- どのようなリファクタリングを提案するのか、具体的に説明してください -->
- フロントエンドで広く利用されている [prettier](https://prettier.io/) を導入して、コードのフォーマットを自動化する
  - 一部 ESLint でフォーマットのチェックをしているところも prettier に寄せたい気持ちです
    https://github.com/digitaldemocracy2030/kouchou-ai/blob/c0a10e33f3f0ea458525a19a55a887b3f3f4792b/client/eslint.config.mjs#L16-L20
    https://github.com/digitaldemocracy2030/kouchou-ai/blob/c0a10e33f3f0ea458525a19a55a887b3f3f4792b/client-admin/eslint.config.mjs#L16-L20
  https://github.com/digitaldemocracy2030/kouchou-ai/blob/c0a10e33f3f0ea458525a19a55a887b3f3f4792b/utils/dummy-server/eslint.config.mjs#L16-L20
- pre-commit or pre-push hook などで prettier を実行する仕組みを導入して、フォーマットされたコードが GitHub に push されるようにする
  - これを実現するツールとしては [husky](https://github.com/typicode/husky) や [lefthook](https://github.com/evilmartians/lefthook) などがありますが、個人的には実行のパフォーマンスと設定のシンプルさから lefthook が良いかなと思っています

**コメント:**

- **shgtkshruch** (2025-03-18T07:01:29Z):

JSX の属性名で curly brace の使い方に揺れがあるので、これも統一したい。（space-between  / auto・1200px のところ）

https://github.com/digitaldemocracy2030/kouchou-ai/blob/1a4bcd162df3cf78865e13db308a14adc8a4ce2d/client/components/Header.tsx#L15

- **yu23ki14** (2025-03-22T08:42:46Z):

> 一部 ESLint でフォーマットのチェックをしているところも prettier に寄せたい気持ちです

こちらbiomeも候補の一つとしてよいかと思いました。Biomeひとつで、prettierとeslintの機能両方いけるはずです。
[移行作業はこちらにまとまっております。](https://biomejs.dev/ja/guides/migrate-eslint-prettier/)
lefthook + biomeで良ければ導入PRつくることもできます。Lint反映はかなり作業量増える気もするので、別issueにするのがいいかもです...

- **shgtkshruch** (2025-03-22T09:47:58Z):

コメントありがとうございます！
自分の issue を立てた趣旨としては、フォーマッターを導入したい意図が強かったので Biome も候補の一つだと思います。

> Biomeひとつで、prettierとeslintの機能両方いけるはず

ESLint も Biome で代替する時に思ったのが、ほとんど問題なく動きそうだなと思いつつ、この辺りのが Biome でもカバーできるかどうかと、
https://github.com/digitaldemocracy2030/kouchou-ai/blob/f91f32817938dc658270abfe0037508f40fd5adf/client/eslint.config.mjs#L13

Next.js が提供している `next lint` が、Lint に加えて Doctoring の機能ももっているので、その機能が Biome で代替できるか（or この機能自体なくても良い？）は気になっていたのですが、この辺りどうですかね？
[Support alternative linters such as Biome · vercel/next.js · Discussion #59347 · GitHub](https://github.com/vercel/next.js/discussions/59347#discussion-5933112)

---

### [(情報整理)Azureについて](https://github.com/digitaldemocracy2030/kouchou-ai/issues/80)

**作成者:** nishio  
**作成日:** 2025-03-18T03:33:26Z  
**内容:**

自治体や大企業などを中心にAzureを使いたいというニーズがある。

これを分解すると2つある

- 1: OpenAIのAPIを直接叩くのではなくAzure OpenAI Serviceを使いたい
- 2: Azureでホストしたい(Azure App Serviceなど)

(1)に関しては実は環境変数USE_AZUREフラグを使った切替が実装されているが、現状の構成に変えた後でのテストが行われていない



**コメント:**

- **nishio** (2025-03-24T16:43:09Z):

https://github.com/digitaldemocracy2030/kouchou-ai/issues/133

---

### [[FEATURE]CSVアップロード時にそれを処理した場合のコストを表示](https://github.com/digitaldemocracy2030/kouchou-ai/issues/79)

**作成者:** nishio  
**作成日:** 2025-03-18T03:19:29Z  
**内容:**

# 背景

>安野貴博: ファイルアップロードすると解析掛ける前にコストを教えてくれるの良さそうですね
>ほづみゆうき: ついにレポート出力まで漕ぎ着けたのですがAPI料金がどれくらいになるのかまったく感覚的に分からずドキドキだったので素人にはあると嬉しいと思います！

# 提案内容

これを実現するためには2つの要素が必要

- 1: done( ~~いまCSVアップロード即処理開始になっているが、一旦確認ダイアログを挟む必要がある~~ )
- 2: どのくらいのデータだとどれくらいの費用になるのかの見積もり関数が必要

## (2)の真面目な作り方

(1)は @nanocloudx さんが詳しいと思うが、(2)の部分がわからなくて着手できないと思う。
UI改善に着手する前に、この関数を作るためのデータ自体を集めていないのでそこからやる必要がある。

- a: extraction
- b: embedding
- c: その後のレポート作成

(a)がO(N)でgpt4oなので大きく、(b)はO(N)だがembedding modelなので安く、cはクラスタ数のオーダー(階層モデルなど今回いろいろ追加したから読めない)という感じで、このそれぞれに分けて料金を出せるようにしてデータ量違いでデータを集めればよい。

## (2)の雑な作り方

ユーザのペインは「すごい高額だったらどうしよう」だと思うので、まず「100円未満っすね」「100~1000円くらい」「これはでかいから1000円以上かかるよ」の3段階でいいのでは説

**コメント:**

- **nasuka** (2025-03-18T04:36:31Z):

@nishio 
ありがとうございます！方針について違和感ないです。

* （2）について、どちらで実装するかは実装者の方にお任せするで良さそうに思いました
  * 真面目な作り方は大変なので一旦雑な作り方で作るでも良さそう
* コスト計算のロジックについては、フロントの実装者の方だとあたりがつかない可能性もあると思うので必要に応じて他の方にお願いするのが良さそう（自分でもOKですし、slackで声がけいただくなどして詳しい方にお願いしても良いかと）

- **nishio** (2025-03-18T08:15:08Z):

すみません、少し理解が古かったようで"いまCSVアップロード即処理開始になっているが、一旦確認ダイアログを挟む必要がある"は間違いで、すでに1ステップ挟むようになってますね！

![Image](https://github.com/user-attachments/assets/b1791d16-6f84-4224-adec-03b4611400a2)

- **nishio** (2025-03-18T09:26:30Z):

aipubcomデータで$0.87でした
comments部分は 4_775_111 bytes

---

### [[FEATURE] ISRによる表示遅延の案内表示](https://github.com/digitaldemocracy2030/kouchou-ai/issues/61)

**作成者:** nanocloudx  
**作成日:** 2025-03-16T08:08:04Z  
**内容:**

# 背景
新しいレポートが生成されてから、閲覧可能になるまでの間には約５分のラグがある
これは client で ISR を行っており、この頻度を 300sec にしているのが原因（この仕組み自体は問題ない認識）
この仕組みを知らないとレポート作成者が迷ってしまうので、５分遅れる旨を client-admin に書くとよさそう

Reference
https://nextjs.org/docs/app/building-your-application/data-fetching/incremental-static-regeneration

# 提案内容
client-admin にレポート生成完了から５分ぐらいは表示できないことがわかる文言を追加する


**コメント:** なし

---

### [[FEATURE]階層図で、最下層の表示を濃いクラスタだけに絞る](https://github.com/digitaldemocracy2030/kouchou-ai/issues/60)

**作成者:** nasuka  
**作成日:** 2025-03-16T07:27:43Z  
**内容:**

# 背景
* 階層図において、最下層のクラスタ数が多すぎるため内容を把握しにくいケースがある


# 提案内容
* 濃いクラスタのフィルタを反映した上で、階層図の最下層クラスタを表示する
  * フィルタはデフォルトで適用しつつ、ON/OFFを切り替えられると良さそう？

**コメント:** なし

---

### [[REFACTOR] langchainの依存を削除する](https://github.com/digitaldemocracy2030/kouchou-ai/issues/58)

**作成者:** nasuka  
**作成日:** 2025-03-16T04:54:26Z  
**内容:**

# 現在の問題点
* 元のtalk to the cityがlangchainに依存していた関係で、kouchou aiでもlangchainを使用してLLM/embedding周りの処理を行っている
* 実装内容としては公式のSDKでも十分処理できるので、不要な依存を外したい

# 提案内容
langchainではなく、openaiの公式SDKを利用する


**コメント:**

- **nishio** (2025-03-20T12:31:16Z):

llm.pyのOpenAIのembeddingだけが残っている状態だと思う

---

### [[FEATURE] 元コメントの表示機能](https://github.com/digitaldemocracy2030/kouchou-ai/issues/56)

**作成者:** nanocloudx  
**作成日:** 2025-03-16T04:00:23Z  
**内容:**

# 背景
現在表示されている文言は、AIが要約した文章(arguments または clusters)である
arguments の生成元となった comments も参照できると良い
（全て表示すると視認性が下がるため、オプションとして表示する項目があると望ましい）

# 提案内容
- hierarchical_result.json に comment を追加する
  - 元コメントは引用がNGの場合があるので、引用元の規約に注意する必要がある
- レポート表示に元コメントを表示するオプションを追加する

**コメント:**

- **ei-blue** (2025-03-25T03:04:40Z):

/assign

#105 と共に対応します。

- **nasuka** (2025-03-28T09:35:30Z):

* 元コメントのデータの中には、再頒布可能なものとそうでないものがある
* 再頒布可能なものは元コメントを紐づけたいが、不可能なものは紐づけられない

-> コメント単位で再頒布可能か否かのフラグを入力データに含めた上で、その表示に問題ないデータのみ散布図上で元コメントを表示するのが良さそう？
問題ないケースについては、以下のスクショのように散布図のツールチップで元コメントを表示する。

![Image](https://github.com/user-attachments/assets/f7b53f2e-13b3-43eb-914a-8d191edebb59)

---

### [[FEATURE] 濃いクラスタのしきい値指定](https://github.com/digitaldemocracy2030/kouchou-ai/issues/55)

**作成者:** nanocloudx  
**作成日:** 2025-03-16T03:55:36Z  
**内容:**

# 背景
現在の濃いクラスタのしきい値は決め打ちである
レポート出力者が、出力結果を確認した上で、適切なしきい値を指定できると良い

# 提案内容
- client-admin にて、出力済みのレポートに対して、しきい値を追加保存できるようにする
- client では濃いクラスタの初期表示が、レポート出力者の指定したしきい値になるようにする

**コメント:** なし

---

### [[FEATURE] GoogleAnalytics 対応](https://github.com/digitaldemocracy2030/kouchou-ai/issues/54)

**作成者:** nanocloudx  
**作成日:** 2025-03-16T03:47:30Z  
**内容:**

# 背景
レポートがどれくらい表示されたのかなど統計を知りたいニーズがありそう

# 提案内容
トラッキングIDを環境変数で指定した場合は、必要なスクリプトが読み込まれるようにする


**コメント:** なし

---

### [[FEATURE] 単一ページの出力機能](https://github.com/digitaldemocracy2030/kouchou-ai/issues/53)

**作成者:** nanocloudx  
**作成日:** 2025-03-16T03:45:56Z  
**内容:**

# 背景
現在はサーバーを起動することで各レポート表示が実現されている
サーバーが用意できない（静的ファイルの配置ならできる）環境でもレポートの公開ができるようにしたい

# 提案内容
next export を用いて単一レポートだけのファイル出力ができる機能を追加する

**コメント:**

- **nishio** (2025-03-25T03:12:13Z):

ゆう猫さんからもどうホスティングしたらいいんだろうという話を聞きました。将来的に静的HTML出力ができるようになると答えたら、それならホストしやすくて助かるとのこと。
結果の公開をしやすくすることで「みんなが使ってレポートを公開している状態」が作られると、認知を集める上でも改善点を見つける上でも好ましいと思いました。

- **nishio** (2025-03-26T10:40:15Z):

Devinはできたって言ってるけどまだレビューできてない
https://github.com/nishio/kouchou-ai/commit/13603c9d6b7da1c34c6d3c8ea774ea760b4eb355

- **shgtkshruch** (2025-03-26T11:37:52Z):

/assign

---

### [[FEATURE] チャート表示に連動した文章表示](https://github.com/digitaldemocracy2030/kouchou-ai/issues/52)

**作成者:** nanocloudx  
**作成日:** 2025-03-16T03:43:03Z  
**内容:**

# 背景
レポートはチャートとクラスター文章から成っている
現在はチャート表示を切り替えたりしても、クラスター文章は初期表示のままである

# 提案内容
表示範囲の更新に合わせて、チャート下部にあるクラスター内容文章(cluster.takeaway)も更新する

**コメント:** なし

---

### [[FEATURE]ストレージ連携](https://github.com/digitaldemocracy2030/kouchou-ai/issues/46)

**作成者:** nasuka  
**作成日:** 2025-03-15T14:01:35Z  
**内容:**

# 変更の背景
* 現在、apiにおいて、各レポートのステータス（ready, etc）と出力されたレポートのファイルは、レポート出力を実行したマシンにのみ保存される
* このため、persistent volumeを持たない実行環境ではapiをホスティングできない
  * また、バックアップを取らない限り、実行環境が壊れた場合にデータが失われてしまう


# 提案内容
* レポートのステータスを記録するファイルと、出力されたレポートおよびその中間ファイルをストレージ（S3等）に連携する
  * 現在、Azureでインフラを構築できるスクリプトが組まれているので、まずはAzure Blob Storageと連携できるようにするのが良さそう？
* 具体的には、以下の処理を実装する
  * ステータスの更新時にステータスファイルをストレージにアップロードする
    * statusファイルは `./server/data/report_status.json` に配置されている
  * レポート出力完了時に、中間ファイル・resultをストレージにアップロードする
    * 中間ファイルは `./server/broadlistening/outputs` 配下に配置されている
      * outputs配下に、各レポートのslugでディレクトリが作成され、そのディレクトリ内にレポートの中間成果物（embeddingやクラスタリング結果など）と結果ファイル（hierarchical_result.json）が格納されている
  * アプリケーション起動時に、ストレージから各ファイルをダウンロードする
* ストレージ連携はオプショナルにする
  * ストレージ利用がオンになっている場合のみストレージ連携を行う



**コメント:**

- **nishio** (2025-03-21T16:03:25Z):

たぶん https://github.com/digitaldemocracy2030/kouchou-ai/issues/53 [FEATURE] 単一ページの出力機能 に依存するタスク

- **nishio** (2025-03-25T08:29:33Z):

ストレージ連携なしで分析して、保存したくなったときにストレージ連携ありに設定を変更してコンテナを作りなおしたタイミングで分析結果が消えるという罠がある
走ってるコンテナをその状態のままでoutputs以下を手元にコピーするといい？

> (理想的な解決方法はわからないけども) apiコンテナのbroadlistening/pipeline/outputsを何らかのコマンドでローカルにコピーして、再起動後に新しいコンテナに再度コピーし直せば一応なんとかなる気がしました
from https://w1740803485-clv347541.slack.com/archives/C08F7JZPD63/p1742889645757549?thread_ts=1742889178.309719&cid=C08F7JZPD63

- **nasuka** (2025-03-25T08:47:15Z):

@nishio 
outputs配下のデータと、 `./server/data/report_status.json` をコピー（& 新コンテナに配置）すれば、新コンテナでもレポートを表示できるはずですね

- **nishio** (2025-03-25T12:45:11Z):

>1.既存のAPIに対して以下を実施
GET /reports を叩いて全レポートのslugを取得する
GET /reports/{slug}を叩いて個別のレポートのresultを取得する
2.新規に構築した環境に以下を実施
outputs配下に各slugの名称でディレクトリを作ってその配下にresultを置く
./server/data/配下のreport_status.jsonを手動で編集する（これを編集しないと一覧画面にレポートが表示されない）

from https://w1740803485-clv347541.slack.com/archives/C08F7JZPD63/p1742904758383619?thread_ts=1742889178.309719&cid=C08F7JZPD63

人間がやるにはちょっと面倒なのでこれをやるscriptを作ってもいいのかも

- **nasuka** (2025-03-26T11:59:48Z):

このイシューでは、Azure Blob Storageと連携できるようにするところまでをスコープにする

---

### [[FEATURE]クラスタ固有の特徴をより捉えたタイトルを生成する](https://github.com/digitaldemocracy2030/kouchou-ai/issues/44)

**作成者:** nasuka  
**作成日:** 2025-03-15T12:58:17Z  
**内容:**

# 変更の背景
* 現状のクラスタリングのタイトル生成処理はクラスタ内部のデータのみを参照している
* このため、内容が似ているクラスタが複数存在する場合に全く同じタイトルが生成されるケースがある


# 提案内容
* クラスタのタイトル生成時に、距離の近いほかのクラスタのデータ点を含め、差分を捉えてタイトルを生成するようにする

**コメント:** なし

---

### [[FEATURE]濃いクラスタを表示している際は、クラスタの説明文も濃いクラスタに合わせたい](https://github.com/digitaldemocracy2030/kouchou-ai/issues/24)

**作成者:** nasuka  
**作成日:** 2025-03-06T05:36:37Z  
**内容:**

# 背景
* 現状は濃いクラスタ表示した際も、全体図と同じクラスタの説明文が並んでいる（最上位層のクラスタが並んでいる）
  * 添付画像のように、現状は散布図上のタイトルと下部のタイトルが整合しない
![Image](https://github.com/user-attachments/assets/27fde824-7e69-4c3d-8f0a-475ca265b20d)

# 提案内容
* 「濃いクラスタ」が選択されている場合はそれらの説明文を表示したい
  * フィルタされているクラスタの解説文のみをページ下部に表示する






**コメント:** なし

---

### [[FEATURE]レポートの複製機能](https://github.com/digitaldemocracy2030/kouchou-ai/issues/19)

**作成者:** nasuka  
**作成日:** 2025-03-04T11:38:39Z  
**内容:**

# 背景
* 設定を少しだけ変えて実行したいケースがある
  * 例えばクラスタ数だけ変えるなど


# 提案内容
* レポートの設定複製機能を実装する


**コメント:**

- **nasuka** (2025-03-04T14:36:51Z):

関連して、レポートの中間成果物（argumentとかembeddingとか）を新規のレポートに引き継げる仕組みはあったほうが良さそう。
クラスタ数を変えるだけなのにextractionを毎回実行すると時間とコストがかかる。

---

### [[FEATURE]階層図ホバー時にクラスタの概要説明を表示したい](https://github.com/digitaldemocracy2030/kouchou-ai/issues/14)

**作成者:** nasuka  
**作成日:** 2025-03-04T11:30:25Z  
**内容:**

# 背景
階層図をホバーしても表示される情報が少なく、クラスタの内容を把握しにくい。


# 提案内容
ホバー時に「クラスタの説明文」をツールチップ表示する
例えば以下のようなクラスタ説明文をツールチップに表示するイメージ

> このクラスタは、生成AIの利用がクリエイターの権利や創作活動に与える影響に関する懸念を集約しています。参加者は、生成AIが著作権を侵害するリスクや、クリエイターの努力を無視することによる創作意欲の減退を指摘し、厳格な規制や法整備の必要性を強調しています。また、生成AIの悪用による名誉毀損や偽情報の拡散、文化的影響についても懸念が示されており、クリエイターとAIの共存を目指すための具体的な対策が求められています。


![Image](https://github.com/user-attachments/assets/c3ccf02e-7701-4ea6-941b-5f73cc15f42e)

**コメント:**

- **shgtkshruch** (2025-03-22T01:47:19Z):

@nasuka 修正の方針について確認させてください。
ツールチップに表示する内容は、「クラスタ説明文」のみにする感じでしょうか？
今のツールチップに表示しているクラスタ名や件数などを残すかどうかが気になっています。

- **nasuka** (2025-03-22T05:26:27Z):

@shgtkshruch 
> 今のツールチップに表示しているクラスタ名や件数などを残すかどうかが気になっています。

説明を入れることによってツールチップの見え方がどうなるかにもよりますが、基本的には残したほうが良いのではないかと思っています！クラスタの内容を把握するうえでは、ツールチップ内に当該クラスタの情報が集約されていた方が良いかなと。
ただ、説明文を入れることによってツールチップの見え方がどうなるか想像がついておらず、いま可視化に使っているplotlyはデザインの柔軟性は余り高くないという話も聞くので、件数/割合の情報を入れることでむしろ見づらくなってしまう場合は情報を落とすことを検討する余地もあるかと思っています。

- **shgtkshruch** (2025-03-22T06:18:22Z):

確認ありがとうございます！
試しに手元の環境で dummy-server のデータをもとに、ツールチップに「クラスタ説明文」を追加してみたのですが、どうでしょうか？

![Image](https://github.com/user-attachments/assets/1fde115c-717a-4c3a-8cd4-b55a418a5a42)

![Image](https://github.com/user-attachments/assets/5f2bfceb-3471-4fd1-a19a-b830915c5a04)


- **nasuka** (2025-03-22T10:37:57Z):

@shgtkshruch 
ありがとうございます！
スクショを拝見して、ツールチップには件数/割合があるとごちゃごちゃしている印象を抱いたので、個人的に件数/割合は省いた方が見やすいと感じました。
UIに関わる部分なので、このあたり @nanocloudx さんにもご意見いただけると助かります！

---

### [[FEATURE]レポート出力の進捗を知りたい](https://github.com/digitaldemocracy2030/kouchou-ai/issues/13)

**作成者:** nasuka  
**作成日:** 2025-03-04T11:15:35Z  
**内容:**

# 背景
* レポート出力が現在どの程度進んでいるのかをダッシュボード上で把握したい


# 提案内容
* バックエンドの処理のステップ単位（extraction, clustering, etc）でダッシュボード上のステータス表示を変える
* 実現方法の案としては、ステップ毎にレポートの実行ステータスを更新する（processingの粒度を細分化する）のが比較的ライトに実現できそう？
  * この場合、以下の実装が必要
    * バックエンド側ではステップを実行する毎にステータスを更新する
    * client/client-admin側でステータスに応じて表示を変える


**コメント:**

- **nishio** (2025-03-19T02:26:42Z):

>バックエンド側ではステップを実行する毎にステータスを更新する

`outputs/<report_id>/status.json`に一応出力されているし、必要そうならもっと扱いやすい形で情報を出すのも可能だと思う

むしろクライアント側をどうするのがいいのか... statusを取得するAPIをつけて2秒に1回pollingするとかかな...

- **nasuka** (2025-03-22T14:12:56Z):

> outputs/<report_id>/status.jsonに一応出力されているし、必要そうならもっと扱いやすい形で情報を出すのも可能だと思う

確かに、status.jsonから情報を取ってくるのは良さそうです！
管理画面を開くユーザーはそこまで多くないでしょうし、負荷もそこまでだと思うのでpollingして更新するアプローチも良さそうに思いました。

---

### [[FEATURE]レポート出力にかかる時間の目安を記載する](https://github.com/digitaldemocracy2030/kouchou-ai/issues/11)

**作成者:** nasuka  
**作成日:** 2025-03-04T10:59:48Z  
**内容:**

# 背景
* レポート出力までに何分程度かかるのかがユーザー目線でわからない


# 提案内容
* 実行時間の目安を記載する


**コメント:** なし

---

