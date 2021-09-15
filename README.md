# Discord Bot

discord内のメッセージ入力欄にコマンドを打ち込むことで,
オンラインゲームの情報や簡易google画像検索を可能にするBot

## 構成

    .
    ├── README.md
    ├── cogs
    │   └── defaultcog.py <- 各コマンドの入出力モジュール
    ├── google_search.py  <- google画像検索にモジュール(google API使用)
    ├── main.py           <- 実行ファイル
    └── riot_api.py       <- オンラインゲーム情報取得モジュール(Riot API使用)

## 実行環境

- python 3.8.0
