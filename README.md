# スプレッドシート Slack リーダー

Google スプレッドシートから Slack の会話データを読み取り、表示用にフォーマットする Python ユーティリティです。

## 説明

このツールは、Slack の会話データを含む指定された Google スプレッドシートに接続します。ワークシート（各 Slack チャンネルを表す）を反復処理し、会話レコードを抽出して読みやすい形式で表示します。このツールはチャンネル参加通知をスキップして、実際の会話内容に焦点を当てます。

https://github.com/kuboon/gsheet-slack-logger

## 前提条件

- Python 3.x
- `gspread` ライブラリ

## セットアップ

1. 必要な Python パッケージをインストールします：
   ```
   pip install gspread
   ```

2. Google Sheets API アクセスを設定します：
   - Google Cloud プロジェクトを作成する
   - Google Sheets API を有効にする
   - サービスアカウントを作成し、JSON キーファイルをダウンロードする
